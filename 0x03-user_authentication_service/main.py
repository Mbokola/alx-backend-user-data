#!/usr/bin/python3
""" Main module
"""

import requests  # type: ignore
import json


base_url = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """ Test for user registration
    """
    user_data = {
        "email": email,
        "password": password
        }
    expected_json = {
        "email": email,
        "message": "user created"
        }
    response = requests.post(base_url + '/users', data=user_data)
    response_json = json.loads(response.text)
    assert (response_json == expected_json)
    expected_json = {
        "message": "email already registered"
        }
    response = requests.post(base_url + '/users', data=user_data)
    response_json = json.loads(response.text)
    assert (response_json == expected_json)


def log_in_wrong_password(email: str, password: str) -> None:
    """ Tests response when wrong password is entered
    """
    user_data = {
        "email": email,
        "password": password
        }
    expected_status_code = 401
    response = requests.post(base_url + "/sessions", data=user_data)
    assert response.status_code == expected_status_code


def log_in(email: str, password: str) -> str:
    """ Tests user login
    """
    user_data = {
        "email": email,
        "password": password
        }
    expected_cookie_name = "session_id"
    response = requests.post(base_url + "/sessions", data=user_data)
    assert expected_cookie_name in response.cookies
    session_id = response.cookies.get("session_id")
    return session_id


def profile_unlogged() -> None:
    """ Test if user is unlogged
    """
    expected_status_code = 403
    response = requests.get(base_url + "/profile")
    assert response.status_code == expected_status_code


def profile_logged(session_id: str) -> None:
    """ Test if user is logged in
    """
    cookies_to_send = {
        "session_id": session_id
        }
    expected_status_code = 200
    response = requests.get(base_url + "/profile", cookies=cookies_to_send)
    assert response.status_code == expected_status_code


def log_out(session_id: str) -> None:
    """ Test user logout
    """
    cookies_to_send = {
        "session_id": session_id
        }
    expected_json = {
        "message": "Bienvenue"
    }
    response = requests.delete(base_url + "/sessions", cookies=cookies_to_send)
    response_json = json.loads(response.text)
    assert response_json == expected_json


def reset_password_token(email: str) -> str:
    """ Test reset password token
    """
    user_data = {
        "email": email
        }
    expected_status_code = 200
    response = requests.post(base_url + "/reset_password", data=user_data)
    assert response.status_code == expected_status_code
    response_json = json.loads(response.text)
    reset_token = response_json['reset_token']
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test for update password functionality
    """
    user_data = {
        "email": email,
        "new_password": new_password
        }
    expected_json = {
        "email": email,
        "message": "Password updated"
        }
    response = requests.put(base_url + "/reset_password", data=user_data)
    response_json = json.loads(response.text)
    assert response_json == expected_json


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
