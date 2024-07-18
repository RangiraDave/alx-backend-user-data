#!/usr/bin/env python3
"""
Auth module
"""

from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Hashes a password with bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a UUID.

    Returns:
        str: The generated UUID.
    """

    return str(uuid4())


class Auth:
    """
    Auth class for interacting with the authentication system.
    """

    def __init__(self) -> None:
        """
        Initialize a new Auth instance.
        """

        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly created User object.
        """

        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a user's login.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login is valid, False otherwise.
        """

        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password,
                    )
        except NoResultFound:
            return False

        return False

    def create_session(self, email: str) -> str:
        """
        Creates a new session for a user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The new session ID.
        """

        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None

        session_id = _generate_uuid()
        self._db.update_user(
            user.id,
            session_id=session_id
            )

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Gets a user from a session ID.
        Args:
            session_id (str): The session ID to look up.
        Returns:
            Union[User, None]: The User object if found, None otherwise.
        """

        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a user's session.
        Args:
            user_id (int): The ID of the user to destroy the session for.
        Returns:
            None
        """

        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a password reset token for a user.
        Args:
            email (str): The email of the user.
        Returns:
            str: The reset token.
        """

        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password given the user's reset token.
        Args:
            reset_token (str): The reset token.
            password (str): The new password.
        Returns:
            None
        """

        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        new_password_hash = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )
        return None
