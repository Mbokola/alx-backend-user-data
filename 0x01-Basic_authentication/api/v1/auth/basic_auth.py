#!/usr/bin/env python3
""" basic_auth module
"""
from .auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class definition
    """
    def __init__(self):
        """ BasicAuth class initialization
        """
        pass

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Extract base64 part of the authorization header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header.split()[1]
