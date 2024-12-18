from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timezone

from src.dynamic_books.schemas import Book, BookResponse, BookUpdateModel
from src.config import db

dynamic_book_router = APIRouter(
    tags = ["CRUD on Book with DataBase"]
)

# Get all books (published and un published) limit to 10 per page and order by created date
@dynamic_book_router.get("", response_description = "Get books", response_model = List[BookResponse])
async def get_all_books(limit : int = 10, order_by : str = "created_at") :

    try :

        books = await db["books"].find().sort(order_by, -1).to_list(limit)
        
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
        new_book = jsonable_encoder(book_data)

        # Add additional informations
        new_book["created_at"] = str(datetime.now(timezone.utc))
        new_book["publisher_user_id"] = "John Doe"
        new_book["status"] = new_book["delete_status"] = False

        new_book = await db["books"].insert_one(new_book)

        created_book = await db["books"].find_one({"_id" : new_book.inserted_id})

        return created_book

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

        book = await db["books"].find_one({"_id" : id, "delete_status" : False})
        
        if book is not None :

            try :

                # Get current time
                timestamp = {"published_at" : datetime.today()}
                book_status = {"status" : True}

                # Change data in JSON
                json_timestamp = jsonable_encoder(timestamp)
                json_book_status = jsonable_encoder(book_status)

                # Merging JSON objects
                book = {**book, **json_timestamp, **json_book_status}

                update_result = await db["books"].update_one({"_id" : id}, {"$set" : book})

                if update_result.modified_count == 1 :

                    if (updated_book := await db["books"].find_one({"_id" : id })) is not None :

                        return updated_book

                if (existing_book := await db["books"].find_one({"_id" : id})) is not None :

                    return existing_book
                
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detal = "The Book with this ID not found"
                )
            
            except Exception as e :

                print(f"Error occurred: {e}")
                
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = f"Internal server error: {str(e)}"
                )
            
        else :

            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "The Book with this ID not found"
            )
    
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
        published_books = await db["books"].find({"status" : True, "delete_status" : False}).sort(order_by, -1).to_list(limit)
        
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

        book = await db["books"].find_one({"_id" : id, "delete_status" : False})
        
        if book is not None :

            if book["status"] == False :

                raise HTTPException(
                    status_code = status.HTTP_304_NOT_MODIFIED,
                    detail = "The Book is already published"
                )
            
            elif book["status"] == True :

                try :

                    # Get current time
                    timestamp = {"unpublished_at" : datetime.today()}
                    book_status = {"status" : False}

                    # Change data in JSON
                    json_timestamp = jsonable_encoder(timestamp)
                    json_book_status = jsonable_encoder(book_status)

                    # Merging JSON objects
                    book = {**book, **json_timestamp, **json_book_status}

                    update_result = await db["books"].update_one({"_id" : id}, {"$set" : book})

                    if update_result.modified_count == 1 :

                        if (updated_book := await db["books"].find_one({"_id" : id })) is not None :

                            return updated_book

                    if (existing_book := await db["books"].find_one({"_id" : id})) is not None :

                        return existing_book
                    
                    raise HTTPException(
                        status_code = status.HTTP_404_NOT_FOUND,
                        detal = "The Book with this ID not found"
                    )
            
                except Exception as e :

                    print(f"Error occurred: {e}")
                    
                    raise HTTPException(
                        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail = f"Internal server error: {str(e)}"
                    )
            
        else :

            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "The Book with this ID not found"
            )
    
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

        unpub_book = await db["books"].find({"status": False, "delete_status" : False}).sort(order_by, -1).to_list(limit)
        
        if unpub_book is not None :

            return unpub_book
            
        else :

            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = "Internal server error"
            )
    
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
        
        book = await db["books"].find_one({"_id" : id, "delete_status" : True})

        if book is not None :

            try :

                # Get current time
                timestamp = {"deleted_at" : datetime.today()}
                book_status = {"delete_status" : True}

                # Change data in JSON
                json_timestamp = jsonable_encoder(timestamp)
                json_book_status = jsonable_encoder(book_status)

                # Merging JSON objects
                book = {**book, **json_timestamp, **json_book_status}

                deleted_result = await db["books"].update_one({"_id" : id}, {"$set" : book})

                if deleted_result.modified_count == 1 :

                    if (deleted_book := await db["books"].find_one({"_id" : id })) is not None :

                        return deleted_book

                if (existing_book := await db["books"].find_one({"_id" : id})) is not None :

                    return existing_book
                
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detal = "The Book with this ID not found"
                )
        
            except Exception as e :

                print(f"Error occurred: {e}")
                
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = f"Internal server error: {str(e)}"
                )

        else :

            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "The Book with this ID not found or The Book is already deleted"
            )
    
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
        
        books = await db["books"].find({"delete_status" : True}).sort(order_by, -1).to_list(limit)
        
        if not books :
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "No deleted book found."
            )

        result = []

        for book in books :

            result.append(BookResponse(**book))

        return result

    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )
        
# Get one book
@dynamic_book_router.get("/{id}", response_description = "Get a book", response_model = BookResponse)
async def get_book(id : str) :

    try :
        book = await db["books"].find_one({"_id" : id, "status" : True, "delete_status" : False})

        if book is None :

            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "The Book with this ID not found"
            )

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

        book = await db["books"].find_one({"_id" : id, "delete_status" : False})

        if book is not None :

            try :

                book_data = {k : v for k, v in book_data.model_dump(exclude_unset=True).items() if v is not None}

                if len(book_data) >=1 :

                    # Get current time
                    timestamp = {"updated_at" : datetime.today()}

                    # Change data in JSON
                    json_timestamp = jsonable_encoder(timestamp)

                    # Merging JSON objects
                    book_data = {**book_data, **json_timestamp}

                    update_result = await db["books"].update_one({"_id" : id}, {"$set" : book_data})

                    if update_result.modified_count == 1 :

                        if (updated_book := await db["books"].find_one({"_id" : id })) is not None :

                            return updated_book

                    if (existing_book := await db["books"].find_one({"_id" : id})) is not None :

                        return existing_book
                    
                    raise HTTPException(
                        status_code = status.HTTP_404_NOT_FOUND,
                        detal = "The Book with this ID not found"
                    )
            
            except Exception as e :

                print(f"Error occurred: {e}")
                
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = f"Internal server error: {str(e)}"
                )

        else :

            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "The Book with this ID not found"
            )
    
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

        book = await db["books"].find_one({"_id" : id})

        if book is not None :

            try :

                delete_result = await db["books"].delete_one({"_id" : id})
                
                if delete_result.deleted_count == 1 :
                    
                    return HTTPException(
                        status_code = status.HTTP_204_NO_CONTENT,
                    )
                
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = "Internal server error"
                )

            except Exception as e :

                print(f"Error occurred: {e}")
        
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = f"Internal server error: {str(e)}"
                )
            
        else :

            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "The Book with this ID not found"
            )

    except Exception as e :

        print(f"Error occurred: {e}")
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error: {str(e)}"
        )
