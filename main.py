from fastapi import FastAPI, Header

app = FastAPI()

# Root Path
@app.get("/")
async def home():
    return {
        "status" : "OK",
        "message" : "Server running"
    }

# Input through URL PATH
# Great user by input
@app.get("/greet/{name}")
async def greet_name(name : str) -> dict :
    return {
        "status" : "OK",
        "message" : f"Hello {name.capitalize()}"
    }

# Input through query parameter
# Great user by input
@app.get("/greet_query")
async def greet_name_query(name : str) -> dict :
    return {
        "status" : "OK",
        "message" : f"Hello {name.capitalize()}"
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
