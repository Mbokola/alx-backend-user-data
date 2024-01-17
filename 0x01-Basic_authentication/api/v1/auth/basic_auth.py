#!/usr/bin/env python3
""" basic_auth module
"""
import base64
from .auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class definition
    """
    def __init__(self):
        """ BasicAuth class initialization
        """
        pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
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

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """ Decodes Base64 string
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            pass
