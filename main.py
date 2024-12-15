from fastapi import FastAPI, Header

app = FastAPI()

# Root Path
@app.get("/")
async def home():
    return {
        "status" : "OK",
        "message" : "Server running"
    }

# Get Headers
@app.get("/get_headers", status_code = 200)
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
