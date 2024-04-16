import secrets
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    """
    This model defines the structure of the response returned when a refresh token request is successful. It includes a new access_token and possibly a new refresh_token.
    """

    access_token: str
    token_type: str = Bearer  # TODO(autogpt): F821 Undefined name `Bearer`
    expires_in: int
    refresh_token: Optional[str] = None


async def refresh_token(refresh_token: str) -> RefreshTokenResponse:
    """
    Refresh the authentication token.

    Args:
        refresh_token (str): The refresh token used to acquire a new access token.

    Returns:
        RefreshTokenResponse: This model defines the structure of the response returned when a refresh token request is successful. It includes a new access_token and possibly a new refresh_token.
    """
    user_key = await prisma.models.ApiKey.prisma().find_unique(
        where={"key": refresh_token}, include={"User": True}
    )
    if user_key is None:
        raise ValueError("Invalid refresh token provided")
    new_access_token = secrets.token_urlsafe(32)
    new_refresh_token = secrets.token_urlsafe(32)
    expires_in = 3600
    await prisma.models.ApiKey.prisma().update(
        where={"id": user_key.id}, data={"key": new_refresh_token}
    )
    return RefreshTokenResponse(
        access_token=new_access_token,
        token_type="Bearer",
        expires_in=expires_in,
        refresh_token=new_refresh_token,
    )
