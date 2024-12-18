from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.home.routes import root_router
from src.books.routes import book_router
from src.web_basics.routes import web_basics_router
from src.dynamic_books.routes import dynamic_book_router

@asynccontextmanager
async def life_span(app:FastAPI) :
    print(f"Server is starting ...")

    yield

    print(f"Server has been stopped")

version = "v1"

app = FastAPI(
    title = "FastBOOK",
    description = "Project to learn FastAPI by creating a book review web service",
    version = version,
    lifespan = life_span
)

app.include_router(root_router)
app.include_router(web_basics_router, prefix=f"/api/{version}/web_basics")
app.include_router(book_router, prefix = f"/api/{version}/books")
app.include_router(dynamic_book_router, prefix = f"/api/{version}/dynamic_books")
