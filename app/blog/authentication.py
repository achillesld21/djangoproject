import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model


class JWTAuthentication(BaseAuthentication):
    """
    Custom authentication class for JWT tokens.
    """
    def authenticate(self, request):
        """
        Authenticates the user based on the JWT in the request's Authorization header.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            tuple: A tuple containing the authenticated user and None for the credentials.

        Raises:
            exceptions.AuthenticationFailed: If the user is not authenticated or the token is invalid.
        """
        # Retrieve the user model
        user_model = get_user_model()

        # Get the Authorization header from the request
        authorization_header = request.headers.get('Authorization')

        # Check if the Authorization header is present
        if not authorization_header:
            return None

        try:
            # Extract the access token from the Authorization header
            access_token = authorization_header.split(' ')[1]

            # Decode the access token's payload
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            # Raise an exception for an expired access token
            raise exceptions.AuthenticationFailed('Access token expired')
        except IndexError:
            # Raise an exception if the token prefix is missing
            raise exceptions.AuthenticationFailed('Token prefix missing')

        # Retrieve the user from the user model using the decoded user ID
        user = user_model.objects.filter(id=payload['user_id']).first()

        # Check if the user exists and is active
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')

        # Return the authenticated user and None for the credentials
        return (user, None)
