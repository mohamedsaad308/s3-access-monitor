from flask import jsonify
from app import app
from utils import categorize_buckets, categorize_objects


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
