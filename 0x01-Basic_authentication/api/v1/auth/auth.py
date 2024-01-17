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
        if excluded_paths and path:
            path = path.rstrip('/')
            excluded_paths = [path.rstrip('/') for path in excluded_paths]
        if not path or not excluded_paths or path not in excluded_paths:
            return True
        if path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """ To be implemented
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        else:
            return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ To be implemented
        """
        return None
