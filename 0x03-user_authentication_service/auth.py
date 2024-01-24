#!/usr/bin/env python3
""" Auth module
"""
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
from typing import Union

import bcrypt  # type: ignore
import uuid


def _hash_password(password: str) -> bytes:
    """ Encrypts user password
    """
    password_byte_encoding = password.encode('utf-8')
    salt = bcrypt.gensalt()
    salted_hashed_passwod = bcrypt.hashpw(password_byte_encoding, salt)

    return salted_hashed_passwod


def _generate_uuid() -> str:
    """ generates a uuid and returns it
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers/creates a new user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            self._db.add_user(email, hashed_password)
            created_user = self._db.find_user_by(email=email)
            return created_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Validatates password against hashed password using bcrypt
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            password_byte_encoding = password.encode('utf-8')
            result = bcrypt.checkpw(password_byte_encoding,
                                    existing_user.hashed_password)

            return result

        except (ValueError, NoResultFound):
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """ Updates the session_id entry of a user in the database
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            existing_user.session_id = session_id
            self._db._session.commit()
            return session_id
        except NoResultFound:
            return None
