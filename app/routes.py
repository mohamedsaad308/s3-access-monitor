from flask import jsonify
from app import app
import boto3
from botocore.exceptions import ClientError
import requests
import concurrent.futures

# Create an S3 client
s3_client = boto3.client("s3")


# Function to categorize buckets as private or public based on Public Access Block settings
def categorize_buckets():
    try:
        # Get a list of all buckets
        buckets = s3_client.list_buckets()["Buckets"]

        # Initialize lists to store private and public buckets
        private_buckets = []
        public_buckets = []

        # Iterate through buckets and categorize based on Public Access Block settings
        for bucket in buckets:
            bucket_name = bucket["Name"]

            # Check the bucket's Public Access Block settings
            public_access_block = s3_client.get_public_access_block(Bucket=bucket_name)
            if all(public_access_block["PublicAccessBlockConfiguration"].values()):
                private_buckets.append(bucket_name)
            else:
                public_buckets.append(bucket_name)

        return private_buckets, public_buckets
    except Exception as e:
        raise e


# View to retrieve and categorize buckets
@app.route("/api/buckets")
def get_buckets():
    try:
        private_buckets, public_buckets = categorize_buckets()

        return jsonify({"private_buckets": private_buckets, "public_buckets": public_buckets})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Function to list objects in a bucket
def list_objs(bucket: str) -> list:
    response = s3_client.list_objects_v2(Bucket=bucket)
    objects = []
    while "Contents" in response:
        for obj_dict in response["Contents"]:
            objects.append(obj_dict["Key"])
        if response["IsTruncated"]:
            response = s3_client.list_objects_v2(Bucket=bucket, StartAfter=objects[-1])
        else:
            break
    return objects


# Function to check if an object is public
def is_public(bucket: str, obj: str) -> bool:
    url = f"https://{bucket}.s3.amazonaws.com/{obj}"
    resp = requests.head(url)
    if resp.status_code == 200:
        return True
    else:
        return False


# Function to categorize objects in a bucket
def categorize_objects():
    private_buckets, public_buckets = categorize_buckets()
    public_objects = []
    private_objects = []

    for bucket in public_buckets:
        for obj in list_objs(bucket):
            if is_public(bucket, obj):
                public_objects.append(
                    {"bucket": bucket, "key": obj, "url": f"https://{bucket}.s3.amazonaws.com/{obj}"}
                )
    for bucket in private_buckets:
        for obj in list_objs(bucket):
            private_objects.append({"bucket": bucket, "key": obj, "url": f"https://{bucket}.s3.amazonaws.com/{obj}"})

    return {
        "public_objects": public_objects,
        "private_objects": private_objects,
        "public_objects_count": len(public_objects),
        "private_objects_count": len(private_objects),
    }


# View to retrieve and categorize objects in buckets
@app.route("/api/categorize-objects", methods=["GET"])
def get_categorized_objects():
    try:
        return jsonify(categorize_objects())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/permissions")
def get_permissions():
    # Logic to fetch and return access permissions of all objects
    permissions = []
    return jsonify(permissions)
