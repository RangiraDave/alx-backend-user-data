#!/usr/bin/env python3
""" Module of Index views

This module contains the views for the index endpoints of the API.
"""

from flask import jsonify, abort
from api.v1.views import app_views


# unauthorized access
@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
  """Handle unauthorized access.

  Returns:
    str: The error message for unauthorized access.
  """

  abort(401, description='Unauthorized')


# forbidden
@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
  """Handle forbidden access.

  Returns:
    str: The error message for forbidden access.
  """
  abort(403, description='Forbidden')


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
  """Handle status request.

  Returns:
    str: The status of the API.
  """

  return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
  """Handle stats request.

  Returns:
    str: The number of each object.
  """

  from models.user import User
  stats = {}
  stats['users'] = User.count()
  return jsonify(stats)
