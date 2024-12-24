from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from typing import List

from fastapi.responses import JSONResponse

from src.dynamic_books.schemas import Book, BookResponse
from src.dynamic_books.services import BookServices

from src.user.dependencies import AccessTokenBearer, RoleChecker
from src.user.utils import get_current_user

book_services = BookServices
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))

dynamic_book_router = APIRouter(tags=["CRUD on Book with DataBase"])


# Get all books (published and un published) limit to 10 per page and order by created date
@dynamic_book_router.get(
    "",
    response_description="Get books",
    response_model=List[BookResponse],
    dependencies=[Depends(RoleChecker(["admin"]))],
)
async def get_all_books(
    limit: int = 10,
    order_by: str = "created_at",
    user_details=Depends(access_token_bearer),
    current_user=Depends(get_current_user),
):

    try:
        books = await book_services.get_all_books(limit, order_by)

        result = []

        if current_user["role"] == "admin":

            if books:

                return books

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "No book published yet"},
            )

        elif current_user["role"] == "user":

            for book in books:

                if current_user == book["publisher_user_id"]:

                    result.append(book)

                else:

                    return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content={"message": "No book published by you"},
                    )

                return result

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


# Create a book
@dynamic_book_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_description="Create a Book",
    response_model=BookResponse,
    dependencies=[role_checker],
)
async def create_a_book(
    book_data: Book,
    user_details=Depends(access_token_bearer),
    current_user=Depends(get_current_user),
) -> dict:

    try:
        new_book = await book_services.create_a_book(book_data, current_user)

        return new_book

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


# Publish a Book
@dynamic_book_router.patch(
    "/publish_book/{id}",
    response_description="Publish a book",
    response_model=BookResponse,
    dependencies=[role_checker],
)
async def publish_a_book(
    id: str,
    user_details=Depends(access_token_bearer),
    current_user=Depends(get_current_user),
):

    try:

        book = await book_services.publish_a_book(id, current_user)

        return book

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


# Get all published books limit to 10 per page and order by created date
@dynamic_book_router.get(
    "/published",
    response_description="Get published books",
    response_model=List[BookResponse],
    dependencies=[role_checker],
)
async def get_all_published_books(
    limit: int = 10,
    order_by: str = "created_at",
    user_details=Depends(access_token_bearer),
    current_user=Depends(get_current_user),
):

    try:

        published_books = await book_services.get_all_published_books(limit, order_by)

        result = []

        if current_user["role"] == "admin":

            if published_books:

                return published_books

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "No book published yet"},
            )

        elif current_user["role"] == "user":

            for book in published_books:

                if current_user == book["publisher_user_id"]:

                    result.append(book)

                else:

                    return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content={"message": "No book published by you"},
                    )

                return result

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


# Unpublish a book
@dynamic_book_router.patch(
    "/unpublish/{id}",
    response_description="Unpublish a book",
    response_model=BookResponse,
    dependencies=[role_checker],
)
async def unpublish_a_book(
    id: str,
    user_details=Depends(access_token_bearer),
    current_user=Depends(get_current_user),
):

    try:

        book = await book_services.unpublish_a_book(id, current_user)

        return book

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


# Get all unpublished books limit to 10 per page and order by created date by user
@dynamic_book_router.get(
    "/unpublished",
    response_description="Get unpublished books",
    response_model=List[BookResponse],
    dependencies=[role_checker],
)
async def get_unpublished_books(
    limit: int = 10,
    order_by: str = "created_at",
    user_details=Depends(access_token_bearer),
    current_user=Depends(get_current_user),
):

    try:

        unpub_books = await book_services.get_unpublished_books(limit, order_by)

        result = []

        if current_user["role"] == "admin":

            return unpub_books

        elif current_user["role"] == "user":

            for book in unpub_books:

                if current_user == book["publisher_user_id"]:

                    result.append(book)

                else:

                    return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content={"message": "No book unpublished by you"},
                    )

                return result

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


# Soft Delete of a Book
@dynamic_book_router.patch(
    "/delete/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete a book",
    dependencies=[role_checker],
)
async def delete_a_book(
    id: str,
    user_details=Depends(access_token_bearer),
    current_user=Depends(get_current_user),
):

    try:

        book = await book_services.delete_a_book(id, current_user)

        return None

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


# Get all deleted books limit to 10 per page and order by created date by user
@dynamic_book_router.get(
    "/all_deleted",
    response_description="Get deleted books",
    response_model=List[BookResponse],
    dependencies=[Depends(RoleChecker(["admin"]))],
)
async def get_deleted_books(
    limit: int = 10,
    order_by: str = "deleted_at",
    user_details=Depends(access_token_bearer),
    current_user=Depends(get_current_user),
):

    try:

        books = await book_services.get_deleted_books(limit, order_by)

        return books

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


# Get one book
@dynamic_book_router.get(
    "/{id}",
    response_description="Get a book",
    response_model=BookResponse,
    dependencies=[role_checker],
)
async def get_a_book(
    id: str,
    user_details=Depends(access_token_bearer),
    current_user=Depends(get_current_user),
):

    try:

        book = await book_services.get_a_book(id)

        if (current_user == book["publisher_user_id"]) or (current_user["role"] == "admin"):

            return book
        
        else:

            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"message": "You are not authorized to perform this action"},
            )

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


# Update a book
@dynamic_book_router.patch(
    "/{id}",
    response_description="Update a book",
    response_model=BookResponse,
    dependencies=[role_checker],
)
async def update_book(
    id: str,
    book_data: Book,
    user_details=Depends(access_token_bearer),
    current_user=Depends(get_current_user),
):

    try:

        book = await book_services.update_book(id, book_data, current_user)

        return book

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


# Get all books for one user
@dynamic_book_router.get(
    "/user_books/{id}",
    response_description="Get one user",
    response_model=List[BookResponse],
    dependencies=[Depends(RoleChecker(["admin"]))],
)
async def get_user_books(
    access_token=Depends(AccessTokenBearer()),
    id: str = "User ID",
    limit: int = 10,
    order_by: str = "created_at",
):

    try:
        books = await book_services.get_user_books(id, limit, order_by)

        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No books found for this user.",
            )

        return books

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


# Hard Delete a book
@dynamic_book_router.delete(
    "/hard_delete/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Hard Delete book",
    dependencies=[Depends(RoleChecker(["admin"]))],
)
async def hard_delete_book(id: str, user_details=Depends(access_token_bearer)):

    try:

        book = await book_services.hard_delete_book(id)

        return None

    except Exception as e:

        print(f"Error occurred: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
