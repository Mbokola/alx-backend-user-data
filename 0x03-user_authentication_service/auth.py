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
