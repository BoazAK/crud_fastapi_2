from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, db, SECRET_KEY
from src.user.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(payload : dict, timestamp : int = None) :
    to_encode = payload.copy()

    if timestamp :
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes = timestamp )
    else :
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES )

    to_encode.update({"exp" : expiration_time})

    jwt_token = jwt.encode(to_encode, key = SECRET_KEY, algorithm = ALGORITHM)

    return jwt_token

def verify_access_token(token: str, credentials_exception):
    try :
        # Decode Token
        payload = jwt.decode(token, key = SECRET_KEY, algorithms = ALGORITHM)
        # Get user ID
        user_id : str = payload.get("id")

        if not user_id : # Same as if user_id is None
            raise credentials_exception
        
        token_data = TokenData(id=user_id)

        return token_data

    except InvalidTokenError :
        raise credentials_exception

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) :
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate token, or token expired",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    
    # Get current user ID
    current_user_id = verify_access_token(token, credentials_exception).id

    # Get current user
    current_user = await db["users"].find_one({"_id" : current_user_id})
    
    return current_user