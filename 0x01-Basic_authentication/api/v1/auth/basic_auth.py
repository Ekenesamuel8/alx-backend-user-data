#!/usr/bin/env python3
""" BasicAuth class module.
"""
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The authorization
            header from the request.

        Returns:
            str: The Base64 part of the header, or None if invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        # Return the part after 'Basic '
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 part of the Authorization header.

        Args:
            base64_authorization_header (str): The Base64 string to decode.

        Returns:
            str: The decoded string, or None if invalid Base64.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode the Base64 string and convert it to a UTF-8 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            # Return None if there's an error in decoding
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user email and password from a Base64 decoded string.

        :param decoded_base64_authorization_header: Base64 decoded string.
        :return: A tuple (user_email, password) or
        (None, None) in case of an error.
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Splitthestringinto email and password usingthefirstoccurrence of":"
        user_email, password = decoded_base64_authorization_header.split(
                ':', 1)

        return user_email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on the given email and password.

        :param user_email: The user's email.
        :param user_pwd: The user's password.
        :return: A User instance if valid
        credentials are provided, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user by email
        users = User.search({"email": user_email})

        if not users or len(users) == 0:
            return None

        # Assuming only one user matches the email, get the first match
        user = users[0]

        # Check if the password is valid
        if not user.is_valid_password(user_pwd):
            return None

        # If the password is correct, return the User instance
        return user
