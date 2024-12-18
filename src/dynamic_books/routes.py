from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timezone

from src.dynamic_books.schemas import Book, BookResponse, BookUpdateModel
from src.config import db

from src.dynamic_books.services import BookServices

book_services = BookServices
dynamic_book_router = APIRouter(
    tags = ["CRUD on Book with DataBase"]
)

# Get all books (published and un published) limit to 10 per page and order by created date
@dynamic_book_router.get("", response_description = "Get books", response_model = List[BookResponse])
async def get_all_books(limit : int = 10, order_by : str = "created_at") :

    try :

        books = await book_services.get_all_books(limit, order_by)
        
        return books
    
    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )

# Create a book
@dynamic_book_router.post("",  status_code = status.HTTP_201_CREATED, response_description = "Create a Book", response_model = BookResponse)
async def create_a_book(book_data : Book) ->  dict :
    try :
        new_book = await book_services.create_a_book(book_data)

        return new_book

    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )

# Publish a Book
@dynamic_book_router.patch("/publish_book/{id}", response_description = "Publish a book", response_model = BookResponse)
async def publish_a_book(id : str) :
        
    try :

        book = await book_services.publish_a_book(id)

        return book
    
    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )

# Get all published books limit to 10 per page and order by created date
@dynamic_book_router.get("/published", response_description = "Get published books", response_model = List[BookResponse])
async def get_all_published_books(limit : int = 10, order_by : str = "created_at") :

    try :

        published_books = await book_services.get_all_published_books(limit, order_by)
        
        return published_books
    
    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )

# Unpublish a book
@dynamic_book_router.patch("/unpublish/{id}", response_description = "Unpublish a book", response_model = BookResponse)
async def unpublish_a_book(id : str) :
        
    try :

        book = await book_services.unpublish_a_book(id)

        return book
    
    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )
    
# Get all unpublished books limit to 10 per page and order by created date by user
@dynamic_book_router.get("/unpublished", response_description = "Get unpublished books", response_model = List[BookResponse])
async def get_unpublished_books(limit : int = 10, order_by : str = "created_at") :
        
    try :

        unpub_book = await book_services.get_unpublished_books(limit, order_by)

        return unpub_book
    
    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )

# Soft Delete of a Book
@dynamic_book_router.patch("/delete/{id}", response_description = "Delete a book")
async def delete_a_book(id : str) :
        
    try :
        
        book = await book_services.delete_a_book(id)

        return book
    
    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )

# Get all deleted books limit to 10 per page and order by created date by user
@dynamic_book_router.get("/all_deleted", response_description = "Get deleted books", response_model = List[BookResponse])
async def get_deleted_books(limit : int = 10, order_by : str = "deleted_at") :

    try :
        
        books = await book_services.get_deleted_books(limit, order_by)

        return books

    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )
        
# Get one book
@dynamic_book_router.get("/{id}", response_description = "Get a book", response_model = BookResponse)
async def get_a_book(id : str) :

    try :

        book = await book_services.get_a_book(id)

        return book
    
    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )
    
# Update a book
@dynamic_book_router.patch("/{id}", response_description = "Update a book", response_model = BookResponse)
async def update_book(id : str, book_data : Book) :

    try :

        book = await book_services.update_book(id, book_data)

        return book
    
    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )
    
# Hard Delete a book
@dynamic_book_router.delete("/hard_delete/{id}", response_description = "Hard Delete book")
async def hard_delete_book(id : str) :
    
    try :

        book = await book_services.hard_delete_book(id)

        return None

    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )
