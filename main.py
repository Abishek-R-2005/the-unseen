import os
import httpx
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend is running"}

@app.get("/calendly/connect")
def calendly_connect():
    client_id = os.getenv("CALENDLY_CLIENT_ID")
    redirect_uri = os.getenv("CALENDLY_REDIRECT_URI")
    authorize_url = (
        "https://auth.calendly.com/oauth/authorize"
        f"?client_id={client_id}"
        "&response_type=code"
        f"&redirect_uri={redirect_uri}"
    )
    return {"authorize_url": authorize_url}

@app.get("/calendly/oauth/callback")
async def calendly_callback(code: str):
    """Exchange code for access token (one-time setup)."""
    token_url = "https://auth.calendly.com/oauth/token"

    data = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("CALENDLY_CLIENT_ID"),
        "client_secret": os.getenv("CALENDLY_CLIENT_SECRET"),
        "redirect_uri": os.getenv("CALENDLY_REDIRECT_URI"),
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(token_url, data=data)
        return resp.json()
