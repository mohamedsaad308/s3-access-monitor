import boto3
import json


# Create an S3 client
def create_client(access_key, secret_key):
    return boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)


# Function to categorize buckets as private or public based on Public Access Block settings
def categorize_buckets(access_key, secret_key):
    # Get a list of all buckets
    s3_client = create_client(access_key, secret_key)
    buckets = s3_client.list_buckets()["Buckets"]

    # Initialize lists to store private and public buckets
    private_buckets = []
    public_buckets = []
    private_buckets_count, publice_buckets_count = 0, 0
    # Iterate through buckets and categorize based on Public Access Block settings
    for bucket in buckets:
        bucket_details = {}
        bucket_details["bucket_name"] = bucket["Name"]
        bucket_acl = s3_client.get_bucket_acl(Bucket=bucket["Name"])
        bucket_details["bucket_acl"] = bucket_acl.get("Grants", {})
        bucket_details["bucket_owner"] = bucket_acl["Owner"].get("DisplayName", "No DisplayName for owner")
        bucket_details["creation_date"] = bucket["CreationDate"].strftime("%Y-%m-%d %H:%M")

        # Check if there is a grant allowing public read access
        for grant in bucket_details["bucket_acl"]:
            grantee = grant.get("Grantee", {})
            uri = grantee.get("URI", "")

            # Check if the grantee is the "AllUsers" group with READ permission
            if uri == "http://acs.amazonaws.com/groups/global/AllUsers" and grant.get("Permission") == "READ":
                bucket_details["acl_is_public"] = True
            else:
                bucket_details["acl_is_public"] = False

        try:
            bucket_policy_response = s3_client.get_bucket_policy(Bucket=bucket["Name"])
            bucket_policy = json.loads(bucket_policy_response["Policy"])
            bucket_details["bucket_policy"] = bucket_policy
        except s3_client.exceptions.from_code("NoSuchBucketPolicy"):
            print(f"Error checking if bucket {bucket['Name']} has a policy!")
            bucket_details["bucket_policy"] = None

        # Check the bucket's Public Access Block settings
        try:
            public_access_block = s3_client.get_public_access_block(Bucket=bucket["Name"])

            if all(public_access_block["PublicAccessBlockConfiguration"].values()):
                private_buckets.append(bucket_details)
                private_buckets_count += 1
            else:
                public_buckets.append(bucket_details)
                publice_buckets_count += 1
        except s3_client.exceptions.from_code("NoSuchBucketPolicy"):
            # We can't access public bucket public access configuration, and we will consider it private
            print(f"Error checking {bucket['Name']} public access configuration!")
            private_buckets.append(bucket_details)
            private_buckets_count += 1

    return {
        "private_buckets": private_buckets,
        "public_buckets": public_buckets,
        "public_buckets_count": publice_buckets_count,
        "private_buckets_count": private_buckets_count,
    }


# Function to list objects in a bucket
def list_objs(bucket: str, s3_client) -> list:
    response = s3_client.list_objects_v2(Bucket=bucket)
    objects = []
    while "Contents" in response:
        for obj_dict in response["Contents"]:
            objects.append(
                {
                    "bucket": bucket,
                    "key": obj_dict["Key"],
                    "size": obj_dict["Size"],
                    "last_modified": obj_dict["LastModified"].strftime("%Y-%m-%d %H:%M"),
                }
            )
        if response["IsTruncated"]:
            response = s3_client.list_objects_v2(Bucket=bucket, StartAfter=objects[-1]["key"])
        else:
            break
    return objects


def is_bucket_public(bucket):
    # Check if the bucket has a public read ACL
    if bucket["acl_is_public"]:
        return True

    # Get the bucket policy and check if it allows public access to all objects
    bucket_policy = bucket["bucket_policy"]
    if not bucket_policy:
        return False

    # Check if the bucket policy allows public access to all objects
    statements = bucket_policy.get("Statement", [])
    for statement in statements:
        if (
            statement.get("Effect") == "Allow"
            and ("s3:GetObject" in statement.get("Action", []) or statement.get("Action", "") == "s3:*")
            and statement.get("Resource", "").endswith(f"{bucket['bucket_name']}/*")
            and statement.get("Principal", "") == "*"
        ):
            return True

    # If no public READ grants or bucket policy allowing public access were found, the bucket is not public
    return False


def is_object_public(bucket, object_name, s3_client):
    try:
        # Check if the bucket that contains the object is publically accessible by ACL
        if bucket["acl_is_public"]:
            # Get the ACL of the object only if the bucket is public by ACL
            acl_response = s3_client.get_object_acl(Bucket=bucket["bucket_name"], Key=object_name)
            grants = acl_response["Grants"]

            # Check if there is a grant allowing public read access
            for grant in grants:
                grantee = grant.get("Grantee", {})
                uri = grantee.get("URI", "")

                # Check if the grantee is the "AllUsers" group with READ permission
                if uri == "http://acs.amazonaws.com/groups/global/AllUsers" and grant.get("Permission") == "READ":
                    return True

        # Get the bucket policy and check if it allows public access to the specific object
        bucket_policy = bucket["bucket_policy"]
        if not bucket_policy:
            return False

        # Check if the bucket policy allows public access to the specific object
        statements = bucket_policy.get("Statement", [])
        for statement in statements:
            resource = statement.get("Resource", "")
            obj_in_rsources = False
            if resource.endswith(f"/{object_name}"):
                obj_in_rsources = True
            elif "/" in object_name and "/" in resource:
                obj_in_rsources = object_name.split("/")[0] in resource.split(":::")[1].split("/")
            else:
                return False

            if (
                statement.get("Effect") == "Allow"
                and ("s3:GetObject" in statement.get("Action", []) or statement.get("Action", "") == "s3:*")
                and obj_in_rsources
                and statement.get("Principal", "") == "*"
            ):
                return True

        # If no public READ grants or bucket policy allowing public access were found, the object is not public
        return False

    except Exception as e:
        print(f"Error checking if object {object_name} in bucket {bucket['bucket_name']} is public: {e}")
        return False


def get_object_url(bucket, obj):
    return f"https://{bucket}.s3.amazonaws.com/{obj}"


# Function to categorize objects in all  buckets
def categorize_objects(all_buckets, access_key, secret_key):
    s3_client = create_client(access_key, secret_key)
    private_buckets, public_buckets = all_buckets.get("private_buckets", []), all_buckets.get("public_buckets", [])
    public_objects = []
    private_objects = []

    for bucket in public_buckets:
        if is_bucket_public(bucket):
            for obj in list_objs(bucket["bucket_name"], s3_client):
                obj["url"] = get_object_url(bucket["bucket_name"], obj["key"])
                public_objects.append(obj)

        else:
            for obj in list_objs(bucket["bucket_name"], s3_client):
                if is_object_public(bucket, obj["key"], s3_client):
                    obj["url"] = get_object_url(bucket["bucket_name"], obj["key"])
                    public_objects.append(obj)
                else:
                    obj["url"] = get_object_url(bucket["bucket_name"], obj["key"])
                    private_objects.append(obj)
    for bucket in private_buckets:
        for obj in list_objs(bucket["bucket_name"], s3_client):
            obj["url"] = get_object_url(bucket["bucket_name"], obj["key"])
            private_objects.append(obj)

    return {
        "public_objects": public_objects,
        "private_objects": private_objects,
        "public_objects_count": len(public_objects),
        "private_objects_count": len(private_objects),
    }


def categorize_bucket_objects(bucket, access_key, secret_key):
    s3_client = create_client(access_key, secret_key)
    bucket_details = {"bucket_name": bucket}
    bucket_acl = s3_client.get_bucket_acl(Bucket=bucket)
    public_access_block = s3_client.get_public_access_block(Bucket=bucket)
    try:
        bucket_policy_response = s3_client.get_bucket_policy(Bucket=bucket)
        bucket_policy = json.loads(bucket_policy_response["Policy"])
        bucket_details["bucket_policy"] = bucket_policy
    except s3_client.exceptions.from_code("NoSuchBucketPolicy"):
        print(f"Error checking if bucket {bucket} has a policy!")
        bucket_details["bucket_policy"] = None
    bucket_details["bucket_acl"] = bucket_acl["Grants"]
    private_buckets = []
    public_buckets = []
    # Check if there is a grant allowing public read access
    for grant in bucket_details["bucket_acl"]:
        grantee = grant.get("Grantee", {})
        uri = grantee.get("URI", "")

        # Check if the grantee is the "AllUsers" group with READ permission
        if uri == "http://acs.amazonaws.com/groups/global/AllUsers" and grant.get("Permission") == "READ":
            bucket_details["acl_is_public"] = True
        else:
            bucket_details["acl_is_public"] = False
        # Check the bucket's Public Access Block settings
        if all(public_access_block["PublicAccessBlockConfiguration"].values()):
            private_buckets.append(bucket_details)
        else:
            public_buckets.append(bucket_details)
        return categorize_objects(
            {
                "private_buckets": private_buckets,
                "public_buckets": public_buckets,
            },
            access_key,
            secret_key,
        )
