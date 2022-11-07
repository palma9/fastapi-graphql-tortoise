import json

import jwt
import requests
from jwt.algorithms import RSAAlgorithm

from app.core.config import settings

JWK_URL = 'https://appleid.apple.com/auth/keys'


def __get_apple_jwk(kid: str) -> str:
    """Get Apple public key from JWK

    Args:
        kid (str): Key ID

    Returns:
        str: Apple key as JWK
    """
    response = requests.get(url=JWK_URL)
    response.raise_for_status()
    keys: dict = response.json().get('keys')

    if not isinstance(keys, list) or not keys:
        raise ValueError('Invalid jwk response')

    if kid:
        return json.dumps([key for key in keys if key['kid'] == kid][0])
    else:
        return (json.dumps(key) for key in keys)


def apple_auth(id_token: str) -> dict:
    """Verify Apple ID token

    Args:
        id_token (str): Apple ID token

    Returns:
        dict: Apple user data
    """
    try:
        kid = jwt.get_unverified_header(id_token).get('kid')
        public_key = RSAAlgorithm.from_jwk(__get_apple_jwk(kid))
        decoded = jwt.decode(
            id_token,
            key=public_key,
            audience=settings.APPLE_CLIENT_ID,
            algorithms=['RS256'],
        )
    except jwt.exceptions.PyJWTError as error:
        raise ValueError(f'Token validation failed by {error}')

    return decoded
