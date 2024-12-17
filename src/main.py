from fastapi import FastAPI

from src.home.routes import root_router
from src.books.routes import book_router
from src.web_basics.routes import web_basics_router

version = "v1"

app = FastAPI(
    title = "FastBOOK",
    description = "Project to learn FastAPI by creating a book review web service",
    version = version,
)

app.include_router(root_router)
app.include_router(web_basics_router, prefix=f"/api/{version}/web_basics")
app.include_router(book_router, prefix = f"/api/{version}/books")
