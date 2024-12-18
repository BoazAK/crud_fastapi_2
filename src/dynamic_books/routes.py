from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timezone

from src.dynamic_books.book_data import books
from src.dynamic_books.schemas import Book, BookResponse, BookUpdateModel
from src.config import db

dynamic_book_router = APIRouter(
    tags = ["CRUD on Book with DataBase"]
)

# Get all posts limit to 10 per page and order by created date
@dynamic_book_router.get("", response_description = "Get blogs content", response_model = List[BookResponse])
async def get_all_books(limit : int = 10, order_by : str = "created_at"):

    try :
        books = await db["books"].find({"status" : False, "delete_status" : False}).sort(order_by, -1).to_list(limit)
        # books = await db["books"].find({"status" : True, "delete_status" : False}).sort(order_by, -1).to_list(limit) # Get books with status True and not deleted

        return books
    
    except Exception as e :
        print(e)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )

# Create a book
@dynamic_book_router.post("",  status_code = status.HTTP_201_CREATED, response_description = "Create Book", response_model = BookResponse)
async def create_a_book(book_data : Book) ->  dict :
    try :
        new_book = jsonable_encoder(book_data)

        # Add additional informations
        new_book["created_at"] = str(datetime.now(timezone.utc))
        new_book["publisher_user_id"] = "John Doe"
        new_book["status"] = new_book["delete_status"] = False

        new_book = await db["books"].insert_one(new_book)

        created_book = await db["books"].find_one({"_id" : new_book.inserted_id})

        return created_book

    except Exception as e :
        print(e)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )

# Get a book
@dynamic_book_router.get("/{book_id}")
async def get_a_book(book_id : int) ->  dict :
    for book in books :
        if book["id"] == book_id :
            return book
        
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Book Not Found"
    )

# Update a book
@dynamic_book_router.patch("/{book_id}")
async def update_a_book(book_id : int, book_update_data : BookUpdateModel) ->  dict :
    for book in books :
        if book["id"] == book_id :
            book["title"] = book_update_data.title
            book["publisher"] = book_update_data.publisher
            book["page_count"] = book_update_data.page_count
            book["language"] = book_update_data.language

            return book
        
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Book Not Found"
    )
    
# Get a book
@dynamic_book_router.delete("/{book_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id : int) :
    for book in books :
        if book["id"] == book_id :
            books.remove(book)

            return {}
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Book Not Found"
    )
