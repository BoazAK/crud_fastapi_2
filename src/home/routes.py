from fastapi import APIRouter
from src.config import ENV

root_router = APIRouter(
    tags = ["API Home"]
)

# Root Path
@root_router.get("/")
async def home() :
    return {
        "status" : "OK",
        "message" : "Server running",
        "environment" : ENV
    }
