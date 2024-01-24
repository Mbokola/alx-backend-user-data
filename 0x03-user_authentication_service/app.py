#!/usr/bin/env python3
""" Flask application
"""
from flask import abort, Flask, request, jsonify
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def root_path():
    """ Root path for Flask application
    """
    return jsonify({
        "message": "Bienvenue"
        })


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """ Handles registration of a user
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        created_user = AUTH.register_user(email, password)

        return jsonify({
            "eamil": created_user.email,
            "message": "user created"
            })
    except ValueError:
        return abort(400)


@app.errorhandler(400)  # type: ignore
def registerd_user(error):
    """ Handles error raised during user regisrtation
    """
    return jsonify({
        "message": "email already registered"
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")  # type: ignore
