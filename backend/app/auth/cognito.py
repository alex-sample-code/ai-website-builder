"""
AWS Cognito client wrapper
"""

import boto3
import hmac
import hashlib
import base64
from typing import Dict, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class CognitoClient:
    """Wrapper for AWS Cognito operations"""

    def __init__(self):
        self.client = boto3.client(
            'cognito-idp',
            region_name=settings.COGNITO_REGION
        )
        self.user_pool_id = settings.COGNITO_USER_POOL_ID
        self.client_id = settings.COGNITO_CLIENT_ID

    def _get_secret_hash(self, username: str) -> str:
        """Calculate secret hash for Cognito (if client secret is used)"""
        # Note: This example assumes no client secret
        # If using client secret, implement the HMAC calculation here
        pass

    async def sign_up(
        self,
        email: str,
        password: str,
        tenant_id: str,
        name: str
    ) -> Dict[str, Any]:
        """
        Register a new user in Cognito

        Args:
            email: User email
            password: User password
            tenant_id: Tenant ID to store as custom attribute
            name: User's full name

        Returns:
            Cognito response with user details
        """
        try:
            response = self.client.sign_up(
                ClientId=self.client_id,
                Username=email,
                Password=password,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'name', 'Value': name},
                    {'Name': 'custom:tenant_id', 'Value': str(tenant_id)},
                ]
            )
            logger.info(f"User signed up successfully: {email}")
            return response
        except Exception as e:
            logger.error(f"Cognito sign up error: {e}")
            raise

    async def confirm_sign_up(self, username: str, confirmation_code: str) -> Dict[str, Any]:
        """Confirm user email with verification code"""
        try:
            response = self.client.confirm_sign_up(
                ClientId=self.client_id,
                Username=username,
                ConfirmationCode=confirmation_code
            )
            return response
        except Exception as e:
            logger.error(f"Cognito confirm sign up error: {e}")
            raise

    async def initiate_auth(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user with email and password

        Args:
            email: User email
            password: User password

        Returns:
            Authentication tokens
        """
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password,
                }
            )
            logger.info(f"User authenticated successfully: {email}")
            return response
        except Exception as e:
            logger.error(f"Cognito authentication error: {e}")
            raise

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token"""
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': refresh_token,
                }
            )
            return response
        except Exception as e:
            logger.error(f"Cognito token refresh error: {e}")
            raise

    async def forgot_password(self, username: str) -> Dict[str, Any]:
        """Initiate forgot password flow"""
        try:
            response = self.client.forgot_password(
                ClientId=self.client_id,
                Username=username
            )
            return response
        except Exception as e:
            logger.error(f"Cognito forgot password error: {e}")
            raise

    async def confirm_forgot_password(
        self,
        username: str,
        confirmation_code: str,
        new_password: str
    ) -> Dict[str, Any]:
        """Confirm forgot password with code and new password"""
        try:
            response = self.client.confirm_forgot_password(
                ClientId=self.client_id,
                Username=username,
                ConfirmationCode=confirmation_code,
                Password=new_password
            )
            return response
        except Exception as e:
            logger.error(f"Cognito confirm forgot password error: {e}")
            raise

    async def get_user(self, access_token: str) -> Dict[str, Any]:
        """Get user details from access token"""
        try:
            response = self.client.get_user(
                AccessToken=access_token
            )
            return response
        except Exception as e:
            logger.error(f"Cognito get user error: {e}")
            raise

    async def update_user_attributes(
        self,
        access_token: str,
        attributes: list[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Update user attributes"""
        try:
            response = self.client.update_user_attributes(
                AccessToken=access_token,
                UserAttributes=attributes
            )
            return response
        except Exception as e:
            logger.error(f"Cognito update user attributes error: {e}")
            raise


# Global instance
cognito_client = CognitoClient()
