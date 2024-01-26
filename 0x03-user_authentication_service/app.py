#!/usr/bin/env python3
""" Flask application
"""
from flask import abort, Flask, request, jsonify, redirect, url_for
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

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
            "email": created_user.email,
            "message": "user created"
            })
    except ValueError:
        return jsonify({
            "message": "email already registered"
            }), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """ Handles user login
    """
    email = request.form.get("email")
    password = request.form.get("password")
    result = AUTH.valid_login(email, password)

    if result:

        session_id = AUTH.create_session(email)
        response = jsonify({
            "email": email,
            "message": "logged in"
            })
        response.set_cookie("session_id", session_id)

        return response

    return abort(401)


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """ Ends a session and logs out user
    """
    session_id = request.cookies.get("session_id")
    record = AUTH.get_user_from_session_id(session_id)

    if record:
        user_id = record.id
        AUTH.destroy_session(user_id)
        return redirect(url_for("root_path"))
    else:
        return abort(403)


@app.route("/profile", strict_slashes=False)
def profile():
    """ gets the user profile
    """
    session_id = request.cookies.get('session_id')
    record = AUTH.get_user_from_session_id(session_id)

    if record:
        return jsonify({
            "email": record.email
            })
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """ handles password reset
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({
            "email": email,
            "reset_token": reset_token
            })
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """ Updates the users' password
    """
    email = request.form.get("email")
    new_password = request.form.get("new_password")
    reset_token = request.form.get("reset_token")

    try:
        AUTH._db.find_user_by(reset_token=reset_token)
        AUTH.update_password(reset_token, new_password)
        return jsonify({
            "email": email,
            "message": "Password updated"
            })
    except (NoResultFound, ValueError):
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")  # type: ignore
