from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

import secrets

from src.user import utils
from src.user.schemas import NewPassword, PasswordReset, User, UserResponse
from src.user.send_email import password_changed, password_reset, send_registration_email
from src.user.utils import create_access_token, get_current_user, get_password_hash

from src.config import db

user_router = APIRouter(
    tags = ["User Routes"]
)

@user_router.post("/registration", response_description = "Register a user")
async def user_registration(user_info: User) :

    try :

        # Get current time
        timestamp = {"created_at" : datetime.now()}

        user_login_status = {"is_logged_in"  : False}
        user_verification_status = {"is_verified" : False}

        # Change data in JSON
        json_timestamp = jsonable_encoder(timestamp)
        json_user_login_status = jsonable_encoder(user_login_status)
        json_user_verification_status = jsonable_encoder(user_verification_status)
        user_info = jsonable_encoder(user_info)

        # Merging JSON objects
        user_info = {**user_info, **json_timestamp, **json_user_login_status, **json_user_verification_status}

        # Find user by username or by email
        user_found = await db["users"].find_one({
            "$or" : [
                {"username" : user_info["username"]},
                {"email" : user_info["email"]}
            ]
        })

        # Raise error if user exist
        if user_found :
            if user_found.get("username") == user_info["username"] :
                raise HTTPException(
                    status_code = status.HTTP_409_CONFLICT,
                    detail = "Username is already taken"
                )
            if user_found.get("email") == user_info["email"] :
                raise HTTPException(
                    status_code = status.HTTP_409_CONFLICT,
                    detail = "Email is already taken"
                )
        
        # Hash user's passowrd
        user_info["password"] = get_password_hash(user_info["password"])

        # Create API Key
        user_info["apiKey"] = secrets.token_hex(30)

        # Save the user
        new_user = await db["users"].insert_one(user_info)
        created_user = await db["users"].find_one({"_id" : new_user.inserted_id})

        if user_info.get("first_name") and user_info.get("last_name") :

            full_name = f'{user_info["first_name"]} {user_info["last_name"]}'
        
        else :

            full_name = user_info["username"]

        # Send email to the user after registration
        await send_registration_email("Registratoin successful", user_info["email"], {
            "title" : "Registration Successfuly",
            "name" : full_name
        })
        
        return {
            "message" : "Account successfully created. A confirmation email has been sent."
        }
    
    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )

@user_router.post("/password_reset_request", response_description = "Password reset request")
async def password_reset_request(user_email : PasswordReset) :
        
    try :
    
        user = await db["users"].find_one({"email" : user_email.email})

        if user is not None :
                
            try :

                token = create_access_token({"id" : user["_id"]}, 5)

                # Local link for password reset
                reset_link = f"http://127.0.0.1:8000/?token={token}"

                # On line link for password reset
                # reset_link = f"https://domain.name/?token={token}"

                timestamp = {"password_reset_request_at" : datetime.today()}

                json_timestamp = jsonable_encoder(timestamp)

                user = {**user, **json_timestamp}

                update_user = await db["users"].update_one({"_id" : user["_id"]}, {"$set" : user})

                if user.get("first_name") and user.get("last_name") :

                    full_name = f"{user['first_name']} {user['last_name']}"
                
                else :

                    full_name = user["username"]

                # Send Email to the user
                await password_reset(
                    "Password reset",
                    user["email"],
                    {
                        "title" : "Password reset",
                        "name" : full_name,
                        "reset_link" : reset_link
                    }
                )
    
            except Exception as e :

                print(f"Error occurred: {e}")
                
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = f"Internal server error: {str(e)}"
                )
        
        else:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "User with this email not found"
            )
    
    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )
    
@user_router.patch("/reset_password", response_description = "Password reset")
async def reset_a_password(token : str, new_password : NewPassword) :
    
    try :
    
        # Pass all the data into dictionary
        request_data = {k : v for k, v in new_password.model_dump().items() if v is not None}

        # Replace the clear password with the hashed one
        request_data["password"] = get_password_hash(request_data["password"])

        # Check if the length of the request is greater than 1
        if len(request_data) >= 1 :
            # Get current user from the token
            user = await get_current_user(token)

            # Get current time
            timestamp = {"password_reset_at" : datetime.today()}
            
            # Change data in JSON
            json_timestamp = jsonable_encoder(timestamp)

            # Merging JSON objects
            request_data = {**request_data, **json_timestamp}

            # Update the user's informations with the password get by the field
            update_result = await db["users"].update_one(
                {"_id" : user["_id"]},
                {"$set" : request_data}
            )

            # Get the currently user updated
            if update_result.modified_count == 1 :
                updated_user = await db["users"].find_one({"_id" : user["_id"]})

                if updated_user is not None :

                    # Local link for login
                    login_link = f"http://127.0.0.1:8000/login"

                    # On line link for login
                    # login_link = f"https://domain.name/login"

                    if user.get("first_name") and user.get("last_name") :

                        full_name = f"{user['first_name']} {user['last_name']}"
                    
                    else :

                        full_name = user["username"]
                    
                    # Send email to the user after password reset
                    await password_changed(
                        "Password changed",
                        user["email"],
                        {
                            "title" : "Password changed",
                            "name" : full_name,
                            "login_link" : login_link
                        }
                    )

        # If nothing is provided, take the existing user
        existing_user = await db["users"].find_one({"_id" : user["_id"]})

        if existing_user is not None :
            return existing_user
        
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User with this email not found"
        )
    
    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )

@user_router.post("/user_login", status_code = status.HTTP_200_OK)
async def user_login(user_credentials: OAuth2PasswordRequestForm = Depends()) :
    
    try :
        
        # Find one user by username or by email
        user = await db["users"].find_one({
            "$or" : [
                {"username": user_credentials.username},
                {"email": user_credentials.username}
            ]
        })

        try :

            # Validate user credentials and create access token
            if user and utils.verify_password(user_credentials.password, user["password"]):
                
                timestamp = {"last_login_at" : datetime.now()}
                user_login_status = {"is_logged_in"  : True}

                # Change data in JSON
                json_timestamp = jsonable_encoder(timestamp)
                json_user_login_status = jsonable_encoder(user_login_status)
                user_info = jsonable_encoder(user)

                # Merging JSON objects
                user_info = {**user_info, **json_timestamp, **json_user_login_status}

                # Create the access token
                access_token = create_access_token({"id" : user["_id"], "email" : user["email"]})

                refresh_token = create_access_token({"id" : user["_id"], "email" : user["email"]}, refresh = True, timestamp = 1440)

                update_user = await db["users"].update_one({"_id" : user["_id"]}, {"$set" : user})

                return JSONResponse(
                    content = {
                        "message" : "Login successful",
                        "token_type" : "bearer",
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                        "user" : {
                            "id" : user["_id"],
                            "email" : user["email"]
                        }
                    }
                )
            
            else :
                raise HTTPException(
                    status_code = status.HTTP_403_FORBIDDEN,
                    detail = "Invalid user credentials",
                    headers = {"WWW-Authenticate": "Bearer"},
                )
    
        except Exception as e :

            print(f"Error occurred: {e}")
            
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = f"Internal server error: {str(e)}"
            )
    
    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )
