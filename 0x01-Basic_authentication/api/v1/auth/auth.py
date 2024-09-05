#!/usr/bin/env python3
"""Authentication class module.
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Auth class for managing API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.

        Returns:
            - True if path is None or excluded_paths is None or empty
            - False if path is in excluded_paths (slash tolerant)
            - True otherwise (authentication is required)
        """
        if path is None:
            return True

        if not excluded_paths or len(excluded_paths) == 0:
            return True

        # Ensure both path and excluded_paths entries are slash-tolerant
        if path[-1] != '/':
            path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the Flask request object.
        For now, this returns None.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the Flask request object.
        For now, this returns None.
        """
        return None
