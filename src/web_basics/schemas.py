
from pydantic import BaseModel

class BookCreateModel(BaseModel):
    title : str
    author : str