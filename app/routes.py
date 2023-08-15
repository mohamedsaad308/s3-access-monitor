from flask import render_template, jsonify
from app import app


@app.route("/")
def index():
    # Implement your dashboard overview template here
    return "Hello World"


@app.route("/api/buckets")
def get_buckets():
    # Logic to fetch and return all buckets
    buckets = []
    return jsonify(buckets)


@app.route("/api/objects")
def get_objects():
    # Logic to fetch and return all objects in all buckets
    objects = []
    return jsonify(objects)


@app.route("/api/permissions")
def get_permissions():
    # Logic to fetch and return access permissions of all objects
    permissions = []
    return jsonify(permissions)
