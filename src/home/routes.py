from fastapi import APIRouter

root_router = APIRouter(
    tags = ["API Home"]
)

# Root Path
@root_router.get("/")
async def home():
    return {
        "status" : "OK",
        "message" : "Server running"
    }
