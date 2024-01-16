#!/usr/bin/env python3
""" auth module
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ This class is the template for all authentication system implemented.
    """

    def __init__(self):
        """ Class initialization
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns boolean
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ To be implemented
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ To be implemented
        """
        return None
