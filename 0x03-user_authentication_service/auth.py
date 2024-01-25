#!/usr/bin/env python3
""" Auth module
"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
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
            created_user = self._db.add_user(email, hashed_password)
           # created_user = self._db.find_user_by(email=email)
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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Gets a user from database based on session_id
        """
        if session_id:
            try:
                record = self._db.find_user_by(session_id=session_id)
                return record
            except NoResultFound:
                return None

        return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroys a user session
        """
        try:
            record = self._db.find_user_by(id=user_id)
            record.session_id = None
            self._db._session.commit()
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ sets and retrieves the reset token
        """
        try:
            record = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            record.reset_token = reset_token
            self._db._session.commit()
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates the user password
        """
        try:
            record = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            record.hashed_password = hashed_password
            record.reset_token = None
            self._db._session.commit()
            return None
        except NoResultFound:
            raise ValueError
