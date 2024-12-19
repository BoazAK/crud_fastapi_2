from redis import asyncio as aioredis
from fastapi import status
from fastapi.exceptions import HTTPException
from src.config import REDIS_PORT, REDIS_HOST

JTI_EXPIRE = 3600

try:
    token_blocklist = aioredis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    token_blocklist.ping()

except aioredis.ConnectionError as e:

    print(f"Error occurred: {e}")

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Could not connect to Redis: {str(e)}",
    )

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", exp=JTI_EXPIRE)


async def token_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(jti)

    return jti is not None
