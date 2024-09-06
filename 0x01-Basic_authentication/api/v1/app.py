#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
# Import Auth and BasicAuth classes
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


# Create an authentication variable based on AUTH_TYPE
auth = None
auth_type = getenv('AUTH_TYPE', None)


# Check the AUTH_TYPE environment variable and create theAppropriateAuth inst
if auth_type == 'basic_auth':
    auth = BasicAuth()  # create an instance of BasicAuth
else:
    auth = Auth()  # create an instance of Auth


@app.errorhandler(401)
def unauthorized(error):
    """Handler for 401 Unauthorized"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


# Method to handle filtering requests before they're processed
@app.before_request
def before_request_handler():
    """Filter each request before processing."""
    if auth is None:
        # If no auth, skip the filtering
        return

    # List of paths that do not require authentication
    excluded_paths = [
            '/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

    # Check if the request path requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        return

    # If no authorization header, raise 401 Unauthorized
    if auth.authorization_header(request) is None:
        abort(401)

    # If the current user is not found, raise 403 Forbidden
    if auth.current_user(request) is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
