"""
JWT token verification for Cognito tokens
"""

import httpx
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError, JWTClaimsError
from fastapi import HTTPException, status
from functools import lru_cache
from app.config import settings
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_cognito_jwks() -> Dict[str, Any]:
    """
    Fetch Cognito JWKS (JSON Web Key Set) and cache it.
    This is used to verify JWT token signatures.
    """
    try:
        response = httpx.get(settings.COGNITO_JWKS_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch Cognito JWKS: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to verify authentication"
        )


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a Cognito JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Get JWKS
        jwks = get_cognito_jwks()

        # Decode the token header to get the key ID
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if not kid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing key ID"
            )

        # Find the matching key in JWKS
        key = None
        for jwk in jwks.get("keys", []):
            if jwk.get("kid") == kid:
                key = jwk
                break

        if not key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: key not found"
            )

        # Verify and decode the token
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=settings.COGNITO_CLIENT_ID,
            issuer=f"https://cognito-idp.{settings.COGNITO_REGION}.amazonaws.com/{settings.COGNITO_USER_POOL_ID}",
        )

        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except JWTClaimsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token claims error: {str(e)}"
        )
    except JWTError as e:
        logger.error(f"JWT verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication error"
        )


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode a JWT token without verification (for development/testing).
    DO NOT use in production!

    Args:
        token: JWT token string

    Returns:
        Decoded token payload
    """
    try:
        return jwt.get_unverified_claims(token)
    except Exception as e:
        logger.error(f"Failed to decode token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
