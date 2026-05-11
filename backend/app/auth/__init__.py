"""
Authentication module
"""

from app.auth.jwt import verify_token, decode_token
from app.auth.deps import (
    get_current_user,
    get_current_tenant,
    get_current_user_and_tenant,
    require_role,
)
from app.auth.cognito import CognitoClient

__all__ = [
    "verify_token",
    "decode_token",
    "get_current_user",
    "get_current_tenant",
    "get_current_user_and_tenant",
    "require_role",
    "CognitoClient",
]
