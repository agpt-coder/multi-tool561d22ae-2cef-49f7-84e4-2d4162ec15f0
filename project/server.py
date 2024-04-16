import logging
from contextlib import asynccontextmanager

import project.authenticate_user_service
import project.refresh_token_service
import project.revoke_token_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="multi tool",
    lifespan=lifespan,
    description="The Multi-Purpose API Toolkit is designed to offer a wide range of functionality through a single endpoint, making it easier for developers to integrate its features without the need for multiple third-party services. The toolkit provides a variety of endpoints including QR Code Generation, Currency Exchange Rate lookup, IP Geolocation services, Image Resizing, Password Strength Checking, Text-to-Speech conversion, Barcode Generation, Email Validation, Time Zone Conversion, URL Preview generation, PDF Watermarking, and converting RSS Feeds into JSON format. This comprehensive suite aims at simplifying and streamlining developers' tasks by providing a versatile set of tools for different needs, all accessible through one unified API.",
)


@app.post(
    "/auth/logout", response_model=project.revoke_token_service.RevokeTokenResponse
)
async def api_post_revoke_token(
    access_token: str,
) -> project.revoke_token_service.RevokeTokenResponse | Response:
    """
    Revoke the authentication token.
    """
    try:
        res = await project.revoke_token_service.revoke_token(access_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/login",
    response_model=project.authenticate_user_service.AuthenticationResponse,
)
async def api_post_authenticate_user(
    username: str, password: str
) -> project.authenticate_user_service.AuthenticationResponse | Response:
    """
    Authenticate users and return an access token.
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(
            username, password
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/refresh", response_model=project.refresh_token_service.RefreshTokenResponse
)
async def api_post_refresh_token(
    refresh_token: str,
) -> project.refresh_token_service.RefreshTokenResponse | Response:
    """
    Refresh the authentication token.
    """
    try:
        res = await project.refresh_token_service.refresh_token(refresh_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
