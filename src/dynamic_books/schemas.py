from typing import Optional
from uuid import uuid4
from bson import ObjectId
from pydantic import BaseModel, Field


# Books Base Model Class
class Book(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex, alias="_id")
    title: str = Field(...)
    description: str = Field(...)
    author_name: str = Field(...)
    publisher: str = Field(...)
    released_at: str = Field(...)
    page_count: int = Field(...)
    language: str = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "The title of the book",
                "description": "A brief description of the book",
                "author_name": "The name of the author of the book",
                "publisher": "The name of the publisher of the book",
                "released_at": "The date when the book was first released",
                "page_count": "The total number of pages in the book",
                "language": "The language in which the book is written",
            }
        }


# Books Response Model Class
class BookResponse(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex, alias="_id")
    title: str = Field(...)
    description: str = Field(...)
    author_name: str = Field(...)
    publisher: str = Field(...)
    released_at: str = Field(...)
    page_count: int = Field(...)
    language: str = Field(...)
    status: bool
    published_at: Optional[str] = None
    unpublished_at: Optional[str] = None
    publisher_user_id: str = Field(...)
    created_at: str = Field(...)
    updated_at: Optional[str] = None
    delete_status: bool
    deleted_at: Optional[str] = None

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "The title of the book",
                "description": "A brief description of the book",
                "author_name": "The name of the author of the book",
                "publisher": "The name of the publisher of the book",
                "released_at": "The date when the book was first released",
                "page_count": "The total number of pages in the book",
                "language": "The language in which the book is written",
                "status": "The current status of the book (e.g., published, unpublished)",
                "published_at": "The date when the book was officially published (optional) on the platform",
                "unpublished_at": "The date when the book was unpublished on the platform, if applicable (optional)",
                "publisher_user_id": "The user ID of the publisher on the platform",
                "created_at": "The date when the book record was created on the platform",
                "updated_at": "The date when the book record was last updated (optional) on the platform",
                "delete_status": "Indicates whether the book record is marked for deletion on the platform",
                "deleted_at": "The date when the book was deleted, if applicable (optional) on the platform",
            }
        }
