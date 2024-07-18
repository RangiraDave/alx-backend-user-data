#!/usr/bin/env python3
"""
Main module
"""

from auth import requests


EMAIL = 'guillaume@holberton.io'
PASSWD = 'b4l0u'
NEW_PASSWD = 't4rt1fl3tt3'
BASE_URL = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    """
    Tests registering a user
    Args:
        email (str): email of the user
        password (str): password of the user
    Returns:
        None
    """

    url = "{}/users".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }

    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {
        'email': email,
        'message': "user created"
        }

    res = requests.post(url, data=body)
    assert res.status_code == 400
    assert res.json() == {
        'message': "email already registered"
        }


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Tests logging in with a wrong password.
    Args:
        email (str): email of the user
        password (str): password of the user
    Returns:
        None
    """

    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Tests logging in.
    Args:
        email (str): email of the user
        password (str): password of the user
    Returns:
        str: session id
    """

    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Tests retrieving profile information whilst logged out.
    Args:
        None
    Returns:
        None
    """

    url = "{}/profile".format(BASE_URL)
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Tests retrieving profile information whilst logged in.
    Args:
        session_id (str): session id
    Returns:
        None
    """

    url = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.get(url, cookies=req_cookies)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """
    Tests logging out of a session.
    Args:
        session_id (str): session id
    Returns:
        None
    """

    url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.delete(url, cookies=req_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    Tests requesting a password reset.
    Args:
        email (str): email of the user
    Returns:
        str: reset token
    """

    url = "{}/reset_password".format(BASE_URL)
    body = {'email': email}
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updates a user's password using the provided reset token.

    Args:
        email (str): The email address of the user.
        reset_token (str): The reset token received by the user.
        new_password (str): The new password to set for the user.

    Raises:
        AssertionError: If the password update fails
        or the response is not as expected.

    Returns:
        None
    """
    url = "{}/reset_password".format(BASE_URL)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    res = requests.put(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


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
