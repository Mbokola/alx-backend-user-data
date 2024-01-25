#!/usr/bin/env python3
"""defines a method _hash_password"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """takes a password and return its encoded bytes"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """returns string rep of a new uuid"""
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password: str = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """returns true of false based on the validation of
        the provided email and password"""
        try:
            user = self._db.find_user_by(email=email)
            user_pass = user.hashed_password
            passwd_check = bcrypt.checkpw(password.encode('utf-8'), user_pass)
            return passwd_check
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Args:
        - email: users email.
        Find user and creates session_id
        Returns:
        - id string
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Args:
        - session_id: session_id related to a user
        Returns:
        - User of the corresponding session_id
        - None if nothing found or session_id is None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroys the session_id of the correspinding
        user based on the user_id provided"""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Args:
        - email: corresponds to a user.
        Returns:
        - token generated for the user.
        - or valueerror exception if user doesn't exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = str(uuid.uuid4())
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound as e:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """updates user's password using reset_token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                    user.id,
                    hashed_password=hashed_password,
                    reset_token=None)
        except NoResultFound:
            raise ValueError
