from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

books = [
  {
    "id": 1,
    "title": "The Hidden Realm",
    "author": "Olivia Harrison",
    "publisher": "Starlight Press",
    "published_date": "2022-05-15",
    "page_count": 312,
    "language": "English"
  },
  {
    "id": 2,
    "title": "Shadows of the Past",
    "author": "Ethan Rivers",
    "publisher": "Darkwing Books",
    "published_date": "2021-11-03",
    "page_count": 287,
    "language": "English"
  },
  {
    "id": 3,
    "title": "Beyond the Horizon",
    "author": "Clara Thompson",
    "publisher": "Silverstone Publishing",
    "published_date": "2019-08-29",
    "page_count": 408,
    "language": "English"
  },
  {
    "id": 4,
    "title": "Echoes of Eternity",
    "author": "James Cooper",
    "publisher": "Celestial Books",
    "published_date": "2020-02-18",
    "page_count": 510,
    "language": "English"
  },
  {
    "id": 5,
    "title": "The City of Thorns",
    "author": "Aiden Blackwood",
    "publisher": "Emberstone Publishing",
    "published_date": "2023-07-22",
    "page_count": 450,
    "language": "English"
  },
  {
    "id": 6,
    "title": "Frostbitten",
    "author": "Nora Grey",
    "publisher": "Icefire Press",
    "published_date": "2021-12-12",
    "page_count": 365,
    "language": "English"
  },
  {
    "id": 7,
    "title": "Crimson Skies",
    "author": "Samuel Drake",
    "publisher": "Hawkwing Books",
    "published_date": "2024-03-05",
    "page_count": 530,
    "language": "English"
  },
  {
    "id": 8,
    "title": "Waves of Tomorrow",
    "author": "Isabella Monroe",
    "publisher": "Horizon Fiction",
    "published_date": "2020-10-17",
    "page_count": 390,
    "language": "English"
  },
  {
    "id": 9,
    "title": "The Last Ember",
    "author": "Felix Donovan",
    "publisher": "Emberfall Publishing",
    "published_date": "2022-01-25",
    "page_count": 295,
    "language": "English"
  },
  {
    "id": 10,
    "title": "The Silent Watcher",
    "author": "Lauren West",
    "publisher": "Nightfall Publishing",
    "published_date": "2023-09-13",
    "page_count": 422,
    "language": "English"
  },
  {
    "id": 11,
    "title": "Moonlit Path",
    "author": "Diana Winter",
    "publisher": "Lunar Press",
    "published_date": "2021-04-06",
    "page_count": 378,
    "language": "English"
  },
  {
    "id": 12,
    "title": "Whispers in the Dark",
    "author": "Michael Steele",
    "publisher": "Vanguard Books",
    "published_date": "2022-03-22",
    "page_count": 422,
    "language": "English"
  },
  {
    "id": 13,
    "title": "Glimmering Shores",
    "author": "Harper Quinn",
    "publisher": "Oceanview Publishing",
    "published_date": "2023-06-14",
    "page_count": 498,
    "language": "English"
  },
  {
    "id": 14,
    "title": "The Dark Tide",
    "author": "Liam Storm",
    "publisher": "Stormwind Publishing",
    "published_date": "2021-10-01",
    "page_count": 357,
    "language": "English"
  },
  {
    "id": 15,
    "title": "Dawn of the Phoenix",
    "author": "Jessica Rivers",
    "publisher": "Phoenix Press",
    "published_date": "2020-09-30",
    "page_count": 488,
    "language": "English"
  },
  {
    "id": 16,
    "title": "Lost Horizons",
    "author": "Nathan Black",
    "publisher": "Mystic Works",
    "published_date": "2022-12-12",
    "page_count": 522,
    "language": "English"
  },
  {
    "id": 17,
    "title": "Bound by Fate",
    "author": "Maya Fields",
    "publisher": "Destiny Books",
    "published_date": "2023-11-21",
    "page_count": 450,
    "language": "English"
  },
  {
    "id": 18,
    "title": "Silver Rain",
    "author": "Elena Hart",
    "publisher": "Winterstone Publishing",
    "published_date": "2020-06-12",
    "page_count": 321,
    "language": "English"
  },
  {
    "id": 19,
    "title": "Through the Flames",
    "author": "Gabriel Stark",
    "publisher": "Ember Books",
    "published_date": "2021-01-15",
    "page_count": 376,
    "language": "English"
  },
  {
    "id": 20,
    "title": "The Silver Crown",
    "author": "Victoria Ashford",
    "publisher": "Royal Gate Publishing",
    "published_date": "2024-01-08",
    "page_count": 399,
    "language": "English"
  },
  {
    "id": 21,
    "title": "The Final Reckoning",
    "author": "Jonas Knight",
    "publisher": "Crimson Crown Press",
    "published_date": "2023-07-30",
    "page_count": 535,
    "language": "English"
  },
  {
    "id": 22,
    "title": "The Golden Hour",
    "author": "Charlotte Pierce",
    "publisher": "Glittering Sea Books",
    "published_date": "2020-02-21",
    "page_count": 482,
    "language": "English"
  },
  {
    "id": 23,
    "title": "Wings of Fire",
    "author": "Katherine Bell",
    "publisher": "Flameworks Publishing",
    "published_date": "2021-04-14",
    "page_count": 393,
    "language": "English"
  },
  {
    "id": 24,
    "title": "A Dance with Shadows",
    "author": "Daniel Grey",
    "publisher": "Nightfall Press",
    "published_date": "2022-09-19",
    "page_count": 460,
    "language": "English"
  },
  {
    "id": 25,
    "title": "The Eternal Flame",
    "author": "Sophie Lane",
    "publisher": "Firestone Publishing",
    "published_date": "2023-03-09",
    "page_count": 509,
    "language": "English"
  },
  {
    "id": 26,
    "title": "Beneath the Moonlight",
    "author": "Max Holloway",
    "publisher": "Moonstone Books",
    "published_date": "2021-06-26",
    "page_count": 421,
    "language": "English"
  },
  {
    "id": 27,
    "title": "The Silent Key",
    "author": "Nina Holt",
    "publisher": "Whisperwind Press",
    "published_date": "2024-02-11",
    "page_count": 397,
    "language": "English"
  },
  {
    "id": 28,
    "title": "Starlight Dreamer",
    "author": "Dylan West",
    "publisher": "Starfire Press",
    "published_date": "2022-07-19",
    "page_count": 463,
    "language": "English"
  },
  {
    "id": 29,
    "title": "The Unseen War",
    "author": "Victor Black",
    "publisher": "Warrior Publishing",
    "published_date": "2020-01-13",
    "page_count": 420,
    "language": "English"
  },
  {
    "id": 30,
    "title": "Tides of Fate",
    "author": "Audrey Stone",
    "publisher": "Tidewater Publishing",
    "published_date": "2023-08-23",
    "page_count": 376,
    "language": "English"
  }
]

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
        "message" : f"Hello {name.title()}"
    }

# Use path parameter and URL query
@app.get("/greet_path_query/{name}")
async def greet_path_query(name : str, age : int) -> dict :
    return {
        "status" : "OK",
        "message" : f"Hello {name.title()}",
        "age" : age
    }

# Use two URL queries and make one optional
@app.get("/greet_path_optional")
async def greet_path_optional(
    name : Optional[str] = "User",
    age : int = 0
    ) -> dict :
    return {
        "status" : "OK",
        "message" : f"Hello {name.title()}",
        "age" : age
    }

class BookCreateModel(BaseModel):
    title : str
    author : str

# Post request
@app.post("/create_book")
async def create_book(book_data : BookCreateModel):
    return {
        "title" : book_data.title,
        "author" : book_data.author
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
