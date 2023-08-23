from flask import jsonify, request
from app import app
from utils import categorize_buckets, categorize_objects
import boto3


# A View to validate AWS credentials
@app.route("/api/validate-aws-credentials", methods=["POST"])
def validate_aws_credentials():
    # Get access key and secret key from the request JSON
    data = request.get_json()
    access_key = data.get("access_key")
    secret_key = data.get("secret_key")

    try:
        # Initialize Boto3 client with provided credentials
        client = boto3.client("sts", aws_access_key_id=access_key, aws_secret_access_key=secret_key)

        # Use get_caller_identity to validate the credentials
        response = client.get_caller_identity()

        # Check if the response contains valid information
        if "Account" in response and "UserId" in response and "Arn" in response:
            return jsonify({"valid": True, "message": "Credentials are valid.", "caller_identity": response})
        else:
            return jsonify({"valid": False, "message": "Invalid credentials."})
    except Exception as e:
        return jsonify({"valid": False, "message": str(e)}), 500


# View to retrieve and categorize buckets
@app.route("/api/buckets")
def get_buckets():
    try:
        return jsonify(categorize_buckets())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
