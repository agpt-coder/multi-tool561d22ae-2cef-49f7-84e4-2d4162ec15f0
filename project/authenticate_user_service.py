from datetime import datetime, timedelta

import prisma
import prisma.models
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class AuthenticationResponse(BaseModel):
    """
    Response model for successful authentication, returning an access token.
    """

    access_token: str
    token_type: str
    expires_in: int


SECRET_KEY = "YOUR_SECRET_KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the given plain password matches the hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password matches, False otherwise.

    """
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str) -> AuthenticationResponse:
    """
    Authenticate users and return an access token.

    Args:
    username (str): The user's username, typically an email address.
    password (str): The user's password.

    Returns:
    AuthenticationResponse: Response model for successful authentication, returning an access token.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if not user:
        return AuthenticationResponse(
            access_token="", token_type="bearer", expires_in=0
        )
    if not await verify_password(password, user.password):
        return AuthenticationResponse(
            access_token="", token_type="bearer", expires_in=0
        )
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(user.id)}
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return AuthenticationResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
