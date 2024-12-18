from pydantic import BaseModel

# Books Base Model Class
class Book(BaseModel) :
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

# Books Update Model Class
class BookUpdateModel(BaseModel) :
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
