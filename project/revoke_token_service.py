import prisma
import prisma.models
from pydantic import BaseModel


class RevokeTokenResponse(BaseModel):
    """
    This model outlines the response after a token revocation attempt. It provides feedback on whether the operation was successful.
    """

    status: str
    message: str


async def revoke_token(access_token: str) -> RevokeTokenResponse:
    """
    Revoke the authentication token.

    This function revokes the provided access token by setting its associated ApiKey entry in the database to inactive.
    It checks if the token exists and is active, revokes it, and updates the ApiKey's status accordingly.
    This process is crucial for ensuring the token can no longer be used for authentication and accessing the API.

    Args:
        access_token (str): The access token that the user wants to revoke.

    Returns:
        RevokeTokenResponse: This model outlines the response after a token revocation attempt. It provides feedback on whether the operation was successful.

    Example:
        revoke_token('your_access_token_here')
        > RevokeTokenResponse(status='success', message='Token successfully revoked.')
    """
    api_key = await prisma.models.ApiKey.prisma().find_unique(
        where={"key": access_token}
    )
    if api_key:
        updated_api_key = await prisma.models.ApiKey.prisma().update(
            where={"id": api_key.id}, data={"key": ""}
        )
        return RevokeTokenResponse(
            status="success", message="Token successfully revoked."
        )
    else:
        return RevokeTokenResponse(
            status="error", message="Token not found or already revoked."
        )
