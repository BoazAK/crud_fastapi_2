from fastapi import APIRouter, Header
from typing import Optional

from src.web_basics.schemas import BookCreateModel

web_basics_router = APIRouter(
    tags = ["Web Basics"]
)

# Input through URL PATH
# Great user by input
@web_basics_router.get("/greet/{name}")
async def greet_name(name : str) -> dict :
    return {
        "status" : "OK",
        "message" : f"Hello {name.capitalize()}"
    }

# Input through query parameter
# Great user by input
@web_basics_router.get("/greet_query")
async def greet_name_query(name : str) -> dict :
    return {
        "status" : "OK",
        "message" : f"Hello {name.title()}"
    }

# Use path parameter and URL query
@web_basics_router.get("/greet_path_query/{name}")
async def greet_path_query(name : str, age : int) -> dict :
    return {
        "status" : "OK",
        "message" : f"Hello {name.title()}",
        "age" : age
    }

# Use two URL queries and make one optional
@web_basics_router.get("/greet_path_optional")
async def greet_path_optional(
    name : Optional[str] = "User",
    age : int = 0
    ) -> dict :
    return {
        "status" : "OK",
        "message" : f"Hello {name.title()}",
        "age" : age
    }

# Post request
@web_basics_router.post("/create_book")
async def create_book(book_data : BookCreateModel):
    return {
        "title" : book_data.title,
        "author" : book_data.author
    }

# Get Headers
@web_basics_router.get("/get_headers", status_code = 200)
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None)
):

    request_headers = {}

    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host

    return request_headers
