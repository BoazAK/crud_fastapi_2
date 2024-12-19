from bson import ObjectId
from typing import Any, Dict, Optional
from pydantic_core import CoreSchema
from pydantic import BaseModel, Field, EmailStr, GetJsonSchemaHandler, field_validator
from uuid import uuid4
import re

class User(BaseModel):
    id : str = Field(default_factory = lambda : uuid4().hex, alias = "_id")
    username : str = Field(...)
    password: str = Field(...)
    email : EmailStr = Field(...)

    @field_validator('username')
    @classmethod
    def name_check(cls, v : str) -> str :
        # Name validation
        # if not v or len(v) < 6 or " " in v :
        if not v or len(v) < 6 :
            raise ValueError("Name length can't be under 6 characters")
            # raise ValueError("Name length can't be under 6 characters or can't contain a space")
        
        return v
    
    @field_validator('email')
    @classmethod
    def email_check(cls, v : str) -> str :
        # Regex for email validation
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Check if the email is correct according to the regex
        if not v or not re.match(regex, v) :
            raise ValueError("Email format is not valid")
        
        return v
    
    @field_validator('password')
    @classmethod
    def password_check(cls, v : str) -> str :
        # Password length validation
        if not v or len(v) < 8 :
            raise ValueError("Password length can't be under 8 characters")
        
       # Check if password contain at least one uppercase letter, one lowercase letter, one number and one special character.
        if not re.search(r'[A-Z]', v) and not re.search(r'[a-z]', v) and not re.search(r'[0-9]', v) and not re.search(r'[@$!%*?&]', v) :
            raise ValueError("Password must contain at least one uppercase letter, one lowercase letter, one number and one special character.")

        return v
    
    class Config :
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId : str}
        json_schema_extra = {
            "example" : {
                "username" : "JohnDoe",
                "email" : "jdoe@example.com",
                "password" : "s3cRet_password"
            }
        }

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema : CoreSchema, handler : GetJsonSchemaHandler
    ) -> Dict[str, Any] :
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(type = "string")
        
        return json_schema

class UserResponse(BaseModel):
    id : str = Field(default_factory = lambda : uuid4().hex, alias = "_id")
    username : str = Field(...)
    email : EmailStr = Field(...)
    first_name : Optional[str] = Field(None)
    last_name : Optional[str] = Field(None)
    
    class Config :
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId : str}
        json_schema_extra = {
            "example" : {
                "username" : "JohnDoe",
                "email" : "jdoe@example.com",
                "first_name": "The first name of the user (e.g. John).",
                "last_name": "The last name of the user (e.g. Doe).",
            }
        }

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema : CoreSchema, handler : GetJsonSchemaHandler
    ) -> Dict[str, Any] :
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(type = "string")
        
        return json_schema

class UserResponseAdmin(BaseModel):
    id : str = Field(default_factory = lambda : uuid4().hex, alias = "_id")
    username : str = Field(...)
    email : EmailStr = Field(...)
    created_at : Optional[str] = None
    is_verified : bool = Field(...)
    verified_at : Optional[str] = None
    first_name : str = Field(...)
    last_name : str = Field(...)
    password_reset_request_at : Optional[str] = None
    password_reset_at : Optional[str] = None
    is_logged_in : bool = Field(...)
    last_login_at : Optional[str] = None
    updated_at : Optional[str] = None
    
    class Config :
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId : str}
        json_schema_extra = {
            "example" : {
                "username" : "JohnDoe",
                "email" : "jdoe@example.com",
                "created_at": "The date and time when the user's account was created.",
                "is_verified": "Indicates whether the user's email has been verified.",
                "verified_at": "The date and time when the user's email was verified.",
                "first_name": "The first name of the user (e.g. John).",
                "last_name": "The last name of the user (e.g. Doe).",
                "password_reset_request_at": "The date and time when the user requested a password reset.",
                "password_reset_at": "The date and time when the user's password was actually reset.",
                "is_logged_in": "Indicates whether the user is currently logged in.",
                "last_login_at": "The date and time when the user last logged in.",
                "updated_at": "The date and time when the user's information was last updated."
            }
        }

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema : CoreSchema, handler : GetJsonSchemaHandler
    ) -> Dict[str, Any] :
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(type = "string")
        
        return json_schema
 
class Token(BaseModel) :
    access_token : str
    token_type : str
    
class TokenData(BaseModel) :
    id : str
    email : EmailStr

class PasswordReset(BaseModel) :
    email : EmailStr = Field(...)

class NewPassword(BaseModel) :
    password : str = Field(...)
    