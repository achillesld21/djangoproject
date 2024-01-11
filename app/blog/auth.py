import datetime
import jwt
from django.conf import settings

def generate_access_token(user):
    """
    Generate an access token for the given user.
    The token includes user ID, username, expiration time, and issue time.
    """
    # Set the expiration time to 5 minutes from the current UTC time
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

    # Payload for the access token
    access_token_payload = {
        'user_id': user.id,
        'user_name': user.username,
        'exp': expiration_time,
        'iat': datetime.datetime.utcnow(),
    }

    # Encode the payload into an access token using the secret key
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return access_token


def generate_refresh_token(user):
    """
    Generate a refresh token for the given user.
    The token includes user ID, username, expiration time, and issue time.
    """
    # Set the expiration time to 7 days from the current UTC time
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)

    # Payload for the refresh token
    refresh_token_payload = {
        'user_id': user.id,
        'user_name': user.username,
        'exp': expiration_time,
        'iat': datetime.datetime.utcnow(),
    }

    # Encode the payload into a refresh token using the secret key
    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token
