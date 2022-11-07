import datetime
from uuid import UUID

import jwt
from fastapi import Request, WebSocket
from fastapi.security import OAuth2PasswordBearer
from graphql import GraphQLError
from passlib.context import CryptContext
from strawberry.types import Info

from app.core.config import settings
from app.core.social_auth.apple import apple_auth
from app.core.social_auth.google import google_auth
from app.models.users import User

security = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    """Hash password

    Args:
        password (str): Password to hash

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(pwd: str, hashed_pwd: str) -> bool:
    """Verify password

    Args:
        pwd (str): Password to verify
        hashed_pwd (str): Hashed password

    Returns:
        bool: True if password is correct, False otherwise
    """
    return pwd_context.verify(pwd, hashed_pwd)


def encode_token(user_id: UUID) -> str:
    """Create JWT user token to authenticate

    Args:
        user_id (UUID): User ID

    Returns:
        str: Encoded token
    """
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
        "sub": str(user_id),
    }
    return jwt.encode(
        payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM
    )


def decode_token(token: str) -> UUID:
    """Decode authentification JWT token

    Args:
        token (str): JWT token

    Returns:
        UUID: User ID
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM]
        )
        return UUID(payload["sub"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Expired signature")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def social_auth(provider: str, access_token: str) -> dict:
    """Verify social auth token

    Args:
        provider (str): Social auth provider
        access_token (str): Social auth access token

    Returns:
        dict: Standarized social auth user data
    """
    if provider == "google":
        google_data = google_auth(access_token)
        return {
            "email": google_data["email"],
            "first_name": google_data.get(
                "given_name", google_data["email"].split("@")[0]
            ),
            "last_name": google_data.get("family_name", ""),
        }
    elif provider == "apple":
        apple_data = apple_auth(access_token)
        return {
            "email": apple_data["email"],
            "first_name": " ".join(apple_data.get("name", "").split(" ")[:1]),
            "last_name": " ".join(apple_data.get("name", "").split(" ")[1:]),
        }
    else:
        raise ValueError("Invalid provider")


class IsAuthenticated:
    auth_required_message = "You must be authenticated to access this resource"
    message = "User is not authenticated"

    async def has_permission(self, _source, info: Info, **_kwargs) -> bool:
        """Check if user is authenticated

        Args:
            _source (Any): Source object
            info (Info): GraphQL info object
            **_kwargs (Any): Keyword arguments

        Returns:
            bool: True if user is authenticated
        """
        request: Request | WebSocket = info.context["request"]
        if "Authorization" not in request.headers:
            raise GraphQLError(self.auth_required_message)
        if not (token := decode_token(request.headers["Authorization"])):
            raise GraphQLError(self.message)

        if not (user := await User.get_or_none(id=token)):
            raise GraphQLError(self.message)
        info.context["user"] = user

        return True
