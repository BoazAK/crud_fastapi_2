from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from typing import Any, Optional, List

from src.user.schemas import User
from src.user.utils import decode_token, get_current_user
from src.user.redis import token_in_blocklist


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:

        creds = await super().__call__(request)

        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail={
                    "error" : "This token is invalid or expired",
                    "resolution" : "Please get a new token"
                }
            )

        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail={
                    "error" : "This token is invalid or has been revoked",
                    "resolution" : "Please get a new token"
                }
            )

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:

        token_data = decode_token(token)

        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:

        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:

        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token",
            )
           
class RoleChecker:
    def __init__(self, allowed_roles:List[str]) -> None:
        
        self.allwed_roles = allowed_roles

    def __call__(self, current_user : User = Depends(get_current_user)) -> Any:
        
        if current_user["role"] in self.allwed_roles :
            
            return True
        
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "You are not allowed to perform this action"
        )
