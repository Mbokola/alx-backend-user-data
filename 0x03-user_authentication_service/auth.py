#!/usr/bin/env python3
""" Auth module
"""
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound

import bcrypt  # type: ignore


def _hash_password(password: str) -> bytes:
    """ Encrypts user password
    """
    password_byte_encoding = password.encode('utf-8')
    salt = bcrypt.gensalt()
    salted_hashed_passwod = bcrypt.hashpw(password_byte_encoding, salt)

    return salted_hashed_passwod


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
