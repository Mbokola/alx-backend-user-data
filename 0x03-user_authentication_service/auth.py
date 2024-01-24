#!/usr/bin/env python3
""" Auth module
"""
import bcrypt  # type: ignore


def _hash_password(password: str) -> bytes:
    """ Encrypts user password
    """
    password_byte_encoding = password.encode('utf-8')
    salt = bcrypt.gensalt()
    salted_hashed_passwod = bcrypt.hashpw(password_byte_encoding, salt)

    return salted_hashed_passwod
