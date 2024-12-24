from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timezone

from src.dynamic_books.schemas import Book, BookResponse
from src.config import db


class BookServices:

    # Get all books (published and un published) limit to 10 per page and order by created date
    async def get_all_books(limit: int = 10, order_by: str = "created_at"):

        books = await db["books"].find().sort(order_by, -1).to_list(limit)

        return books

    # Create a book
    async def create_a_book(book_data: Book, current_user : str) -> dict:

        new_book = jsonable_encoder(book_data)

        # Add additional informations
        new_book["publisher_user_id"] = current_user["_id"]
        new_book["created_at"] = str(datetime.now(timezone.utc))
        new_book["status"] = new_book["delete_status"] = False

        new_book = await db["books"].insert_one(new_book)

        created_book = await db["books"].find_one({"_id": new_book.inserted_id})

        return created_book

    # Publish a Book
    async def publish_a_book(id: str, current_user):

        book = await db["books"].find_one({"_id": id, "delete_status": False, "deleted_by_admin": False})

        if book is not None:

            try:

                # Get current time
                timestamp = {"published_at": datetime.today()}
                book_status = {"status": True}

                # Change data in JSON
                json_timestamp = jsonable_encoder(timestamp)
                json_book_status = jsonable_encoder(book_status)

                # Merging JSON objects
                book = {**book, **json_timestamp, **json_book_status}

                if current_user["_id"] == book["publisher_user_id"]:
        
                    update_result = await db["books"].update_one(
                        {"_id": id}, {"$set": book}
                    )
                
                if current_user["role"] == "admin":

                    # Get current updated_by_admin
                    admin_timestamp = {"published_by_admin_at": datetime.today()}
                    admin_publish_status = {"published_by_admin" : True}

                    # Change data in JSON
                    json_timestamp = jsonable_encoder(admin_timestamp)
                    json_status = jsonable_encoder(admin_publish_status)

                    # Merging JSON objects
                    book = {**book, **json_timestamp, **json_status}

                    update_result = await db["books"].update_one(
                        {"_id": id}, {"$set": book}
                    )

                if update_result.modified_count == 1:

                    if (
                        updated_book := await db["books"].find_one({"_id": id})
                    ) is not None:

                        return updated_book

                if (
                    existing_book := await db["books"].find_one({"_id": id})
                ) is not None:

                    return existing_book

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detal="The Book with this ID not found",
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
                detail="The Book with this ID not found",
            )

    # Get all published books limit to 10 per page and order by created date
    async def get_all_published_books(limit: int = 10, order_by: str = "created_at"):

        published_books = (
            await db["books"]
            .find({"status": True, "delete_status": False, "deleted_by_admin": False})
            .sort(order_by, -1)
            .to_list(limit)
        )

        return published_books

    # Unpublish a book
    async def unpublish_a_book(id: str, current_user):

        book = await db["books"].find_one({"_id": id, "delete_status": False, "deleted_by_admin": False})

        if book is not None:

            if book["status"] == True:

                try:

                    # Get current time
                    timestamp = {"unpublished_at": datetime.today()}
                    book_status = {"status": False}

                    # Change data in JSON
                    json_timestamp = jsonable_encoder(timestamp)
                    json_book_status = jsonable_encoder(book_status)

                    # Merging JSON objects
                    book = {**book, **json_timestamp, **json_book_status}

                    if current_user["_id"] == book["publisher_user_id"]:
            
                        update_result = await db["books"].update_one(
                            {"_id": id}, {"$set": book}
                        )
                    
                    if current_user["role"] == "admin":

                        # Get current updated_by_admin
                        admin_timestamp = {"unpublished_by_admin_at": datetime.today()}
                        admin_unpublish_status = {"unpublished_by_admin" : True}

                        # Change data in JSON
                        json_timestamp = jsonable_encoder(admin_timestamp)
                        json_status = jsonable_encoder(admin_unpublish_status)

                        # Merging JSON objects
                        book = {**book, **json_timestamp, **json_status}

                        update_result = await db["books"].update_one(
                            {"_id": id}, {"$set": book}
                        )

                    if update_result.modified_count == 1:

                        if (
                            updated_book := await db["books"].find_one({"_id": id})
                        ) is not None:

                            return updated_book

                    if (
                        existing_book := await db["books"].find_one({"_id": id})
                    ) is not None:

                        return existing_book

                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detal="The Book with this ID not found",
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
                detail="The Book with this ID not found or The Book is already published",
            )

    # Get all unpublished books limit to 10 per page and order by created date by user
    async def get_unpublished_books(limit: int = 10, order_by: str = "created_at"):

        unpub_book = (
            await db["books"]
            .find({"status": False, "delete_status": False, "deleted_by_admin": False})
            .sort(order_by, -1)
            .to_list(limit)
        )

        if unpub_book is not None:

            return unpub_book

        else:

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    # Soft Delete of a Book
    async def delete_a_book(id: str, current_user):

        book = await db["books"].find_one({"_id": id, "delete_status": False, "deleted_by_admin": False})

        if book is not None:

            try:

                # Get current time
                timestamp = {"deleted_at": datetime.today()}
                book_status = {"delete_status": True}

                # Change data in JSON
                json_timestamp = jsonable_encoder(timestamp)
                json_book_status = jsonable_encoder(book_status)

                # Merging JSON objects
                book = {**book, **json_timestamp, **json_book_status}

                if current_user["_id"] == book["publisher_user_id"]:
        
                    deleted_result = await db["books"].update_one(
                        {"_id": id}, {"$set": book}
                    )
                
                if current_user["role"] == "admin":

                    # Get current updated_by_admin
                    admin_timestamp = {"deleted_by_admin_at": datetime.today()}
                    admin_delete_status = {"deleted_by_admin" : True}

                    # Change data in JSON
                    json_timestamp = jsonable_encoder(admin_timestamp)
                    json_status = jsonable_encoder(admin_delete_status)

                    # Merging JSON objects
                    book = {**book, **json_timestamp, **json_status}

                    deleted_result = await db["books"].update_one(
                        {"_id": id}, {"$set": book}
                    )

                if deleted_result.modified_count == 1:

                    if (
                        deleted_book := await db["books"].find_one({"_id": id})
                    ) is not None:

                        return deleted_book

                if (
                    existing_book := await db["books"].find_one({"_id": id})
                ) is not None:

                    return existing_book

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detal="The Book with this ID not found",
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
                detail="The Book with this ID not found or The Book is already deleted",
            )

    # Get all deleted books limit to 10 per page and order by created date by user
    async def get_deleted_books(limit: int = 10, order_by: str = "deleted_at"):

        books = (
            await db["books"]
            .find({"delete_status": True})
            .sort(order_by, -1)
            .to_list(limit)
        )

        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No deleted book found."
            )

        result = []

        for book in books:

            result.append(BookResponse(**book))

        return result

    # Get one book
    async def get_a_book(id: str):

        book = await db["books"].find_one(
            {"_id": id, "delete_status": False, "deleted_by_admin": False}
        )

        if book is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The Book with this ID not found",
            )

        return book

    # Update a book
    async def update_book(id: str, book_data: Book, current_user):

        book = await db["books"].find_one({"_id": id, "delete_status": False, "deleted_by_admin": False})

        if book is not None:

            try:

                book_data = {
                    k: v
                    for k, v in book_data.model_dump(exclude_unset=True).items()
                    if v is not None
                }

                if len(book_data) >= 1:

                    # Get current time
                    timestamp = {"updated_at": datetime.today()}

                    # Change data in JSON
                    json_timestamp = jsonable_encoder(timestamp)

                    # Merging JSON objects
                    book_data = {**book_data, **json_timestamp}

                    if current_user["_id"] == book["publisher_user_id"]:
            
                        update_result = await db["books"].update_one(
                            {"_id": id}, {"$set": book_data}
                        )
                    
                    if current_user["role"] == "admin":

                        # Get current updated_by_admin
                        timestamp = {"updated_by_admin_at": datetime.today()}
                        status = {"updated_by_admin" : True}

                        # Change data in JSON
                        json_timestamp = jsonable_encoder(timestamp)
                        json_status = jsonable_encoder(status)

                        # Merging JSON objects
                        book_data = {**book_data, **json_timestamp, **json_status}

                        update_result = await db["books"].update_one(
                            {"_id": id}, {"$set": book_data}
                        )

                    if update_result.modified_count == 1:

                        if (
                            updated_book := await db["books"].find_one({"_id": id})
                        ) is not None:

                            return updated_book

                    if (
                        existing_book := await db["books"].find_one({"_id": id})
                    ) is not None:

                        return existing_book

                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detal="The Book with this ID not found",
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
                detail="The Book with this ID not found",
            )
        
    async def get_user_books(id, limit, order_by):

        try:
            books = await db["books"].find({"publisher_user_id": id}).sort(order_by, -1).to_list(limit)

            if not books :
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "No books found for this user."
                )

            return books

        except Exception as e:

            print(f"Error occurred: {e}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}",
            )

    # Hard Delete a book
    async def hard_delete_book(id: str):

        book = await db["books"].find_one({"_id": id})

        if book is not None:

            try:

                delete_result = await db["books"].delete_one({"_id": id})

                if delete_result.deleted_count == 1:

                    return HTTPException(
                        status_code=status.HTTP_204_NO_CONTENT,
                    )

                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error",
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
                detail="The Book with this ID not found",
            )
