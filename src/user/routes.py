from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

import httpx, secrets

from src.user.dependencies import RefreshTokenBearer, AccessTokenBearer, RoleChecker
from src.user.schemas import NewPassword, PasswordReset, User, UserResponse
from src.user.send_email import (
    password_changed,
    password_reset,
    send_registration_email,
)
from src.user.utils import create_access_token, get_current_user, get_password_hash, verify_password
from src.user.redis import add_jti_to_blocklist

from src.config import db, DOMAIN_NAME, PORT

role_checker = RoleChecker(["admin", "user"]) 

user_router = APIRouter(tags=["User Routes"])


@user_router.post("/registration", response_description="Register a user")
async def user_registration(user_info: User):

    try:

        # Get current time
        timestamp = {"created_at": datetime.now()}
        user_login_status = {"is_logged_in": False}
        user_verification_status = {"is_verified": False}
        user_role = {"role": "user"}

        # Change data in JSON
        json_timestamp = jsonable_encoder(timestamp)
        json_user_login_status = jsonable_encoder(user_login_status)
        json_user_verification_status = jsonable_encoder(user_verification_status)
        json_user_role = jsonable_encoder(user_role)
        user_info = jsonable_encoder(user_info)

        # Merging JSON objects
        user_info = {
            **user_info,
            **json_timestamp,
            **json_user_login_status,
            **json_user_verification_status,
            **json_user_role,
        }

        # Find user by username or by email
        user_found = await db["users"].find_one(
            {
                "$or": [
                    {"username": user_info["username"]},
                    {"email": user_info["email"]},
                ]
            }
        )

        # Raise error if user exist
        if user_found:
            if user_found.get("username") == user_info["username"]:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username is already taken",
                )
            if user_found.get("email") == user_info["email"]:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email is already taken",
                )

        # Hash user's passowrd
        user_info["password"] = get_password_hash(user_info["password"])

        # Create API Key
        user_info["apiKey"] = secrets.token_hex(30)

        # Save the user
        new_user = await db["users"].insert_one(user_info)
        created_user = await db["users"].find_one({"_id": new_user.inserted_id})

        if user_info.get("first_name") and user_info.get("last_name"):

            full_name = f'{user_info["first_name"]} {user_info["last_name"]}'

        else:

            full_name = user_info["username"]

        # Send email to the user after registration
        await send_registration_email(
            "Registratoin successful",
            user_info["email"],
            {"title": "Registration Successfuly", "name": full_name},
        )

        return {
            "message": "Account successfully created. A confirmation email has been sent."
        }

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@user_router.post(
    "/password_reset_request", response_description="Password reset request"
)
async def password_reset_request(user_email: PasswordReset):

    try:

        user = await db["users"].find_one({"email": user_email.email})

        if user is not None:

            try:

                token = create_access_token({"id": user["_id"]}, 5)

                # Local link for password reset
                reset_link = f"http://{DOMAIN_NAME}:{PORT}/?token={token}"

                # On line link for password reset
                # reset_link = f"https://{DOMAIN_NAME}/?token={token}"

                timestamp = {"password_reset_request_at": datetime.today()}

                json_timestamp = jsonable_encoder(timestamp)

                user = {**user, **json_timestamp}

                update_user = await db["users"].update_one(
                    {"_id": user["_id"]}, {"$set": user}
                )

                if user.get("first_name") and user.get("last_name"):

                    full_name = f"{user['first_name']} {user['last_name']}"

                else:

                    full_name = user["username"]

                # Send Email to the user
                await password_reset(
                    "Password reset",
                    user["email"],
                    {
                        "title": "Password reset",
                        "name": full_name,
                        "reset_link": reset_link,
                    },
                )

            except Exception as e:

                print(f"Error occurred: {e}")

                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Internal server error: {str(e)}",
                )

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email not found",
            )

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@user_router.patch("/reset_password", response_description="Password reset")
async def reset_a_password(token: str, new_password: NewPassword):

    try:

        # Pass all the data into dictionary
        request_data = {
            k: v for k, v in new_password.model_dump().items() if v is not None
        }

        # Replace the clear password with the hashed one
        request_data["password"] = get_password_hash(request_data["password"])

        # Check if the length of the request is greater than 1
        if len(request_data) >= 1:
            # Get current user from the token
            user = await get_current_user(token)

            # Get current time
            timestamp = {"password_reset_at": datetime.today()}

            # Change data in JSON
            json_timestamp = jsonable_encoder(timestamp)

            # Merging JSON objects
            request_data = {**request_data, **json_timestamp}

            # Update the user's informations with the password get by the field
            update_result = await db["users"].update_one(
                {"_id": user["_id"]}, {"$set": request_data}
            )

            # Get the currently user updated
            if update_result.modified_count == 1:
                updated_user = await db["users"].find_one({"_id": user["_id"]})

                if updated_user is not None:

                    # Local link for login
                    login_link = f"http://{DOMAIN_NAME}:{PORT}/login"

                    # On line link for login
                    # login_link = f"https://{DOMAIN_NAME}/login"

                    if user.get("first_name") and user.get("last_name"):

                        full_name = f"{user['first_name']} {user['last_name']}"

                    else:

                        full_name = user["username"]

                    # Send email to the user after password reset
                    await password_changed(
                        "Password changed",
                        user["email"],
                        {
                            "title": "Password changed",
                            "name": full_name,
                            "login_link": login_link,
                        },
                    )

        # If nothing is provided, take the existing user
        existing_user = await db["users"].find_one({"_id": user["_id"]})

        if existing_user is not None:
            return existing_user

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email not found",
        )

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@user_router.post("/user_login", status_code=status.HTTP_200_OK)
async def user_login(user_credentials: OAuth2PasswordRequestForm = Depends()):

    try:

        # Find one user by username or by email
        user = await db["users"].find_one(
            {
                "$or": [
                    {"username": user_credentials.username},
                    {"email": user_credentials.username},
                ]
            }
        )

        try:

            # Validate user credentials and create access token
            if user and verify_password(
                user_credentials.password, user["password"]
            ):

                timestamp = {"last_login_at": datetime.now()}
                user_login_status = {"is_logged_in": True}

                # Change data in JSON
                json_timestamp = jsonable_encoder(timestamp)
                json_user_login_status = jsonable_encoder(user_login_status)
                user_info = jsonable_encoder(user)

                # Merging JSON objects
                user_info = {**user_info, **json_timestamp, **json_user_login_status}

                # Create the access token
                access_token = create_access_token(
                    {"id": user["_id"], "email": user["email"], "role":user["role"]}
                )

                refresh_token = create_access_token(
                    {"id": user["_id"], "email": user["email"], "role":user["role"]},
                    refresh=True,
                    timestamp=172800,
                )

                update_user = await db["users"].update_one(
                    {"_id": user["_id"]}, {"$set": user_info}
                )

                return JSONResponse(
                    content={
                        "message": "Login successful",
                        "token_type": "bearer",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": {"id": user["_id"], "email": user["email"]},
                    }
                )

            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid user credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        except Exception as e:

            print(f"Error occurred: {e}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}",
            )

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@user_router.get("/refresh_token")
async def get_new_access_token(
    token_details: dict = Depends(RefreshTokenBearer()), access_token : str = "Access Token"
):
    
    url = f"http://{DOMAIN_NAME}:{PORT}/api/v1/user/me"

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {str(access_token)}'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch user info")
    
    if (user_info["is_logged_in"] == True) and (user_info["_id"] == token_details["id"]) and (user_info["email"] == token_details["email"]):

        expiry_timestamp = token_details["exp"]

        if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
            new_access_token = create_access_token(
                {"id": token_details["id"], "email": token_details["email"]}
            )
            new_refresh_token = create_access_token(
                {"id": token_details["id"], "email": token_details["email"]},
                refresh=True,
                timestamp=172800,
            )

            jti = token_details["jti"]

            await add_jti_to_blocklist(jti)

            return JSONResponse(
                content={
                    "access_token": new_access_token,
                    "refresh_token": new_refresh_token
                }
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action"
        )

@user_router.get("/me")
async def get_current_user_infos(current_user=Depends(get_current_user), access_token: dict = Depends(AccessTokenBearer()), _: bool = Depends(role_checker)):

    return current_user

@user_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):

    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Logged out successfully"}
    )

@user_router.get("/users")
