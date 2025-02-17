#!/usr/bin/env python3
"""
Route module for the API
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")

if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def before_request():
    """
    Function to be executed before each request.

    If authentication is enabled, it checks if the request requires
    authentication
    and if the user is authorized to access the requested resource.
    """

    if auth is None:
        pass
    else:
        excluded_list = ['/api/v1/status/',
                         '/api/v1/unauthorized/', '/api/v1/forbidden/']

        if auth.require_auth(request.path, excluded_list):
            if auth.authorization_header(request) is None:
                abort(401, description="Unauthorized")
            if auth.current_user(request) is None:
                abort(403, description='Forbidden')


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Error handler for 401 Unauthorized status code.

    Args:
        error: The error object.

    Returns:
        A JSON response with the error message.
    """

    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Error handler for 403 Forbidden status code.

    Args:
        error: The error object.

    Returns:
        A JSON response with the error message.
    """

    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Error handler for 404 Not Found status code.

    Args:
        error: The error object.

    Returns:
        A JSON response with the error message.
    """

    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
