from fastapi import FastAPI, Header, HTTPException, status
import asyncio

from models import get_random_kuwiki

app = FastAPI()

KUWIKI_ENDPOINT = '/api/course'

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get(KUWIKI_ENDPOINT)
async def get_kakomon_url(name: str, authorization:str|None= Header(default=None)):
    if authorization is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No authorization header")

    if authorization != "Token 1234abcd":
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")

    kuwiki = get_random_kuwiki(name)
    await asyncio.sleep(0.3)
    return kuwiki
