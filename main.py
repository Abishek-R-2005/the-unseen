import httpx
from fastapi import FastAPI

app = FastAPI()

# <<< TEMP: hard-coded Calendly app credentials >>>
CALENDLY_CLIENT_ID = "YeeYevrFdj0m_oqL4bXsOns8ztDdkImhQ8QvF9DRHbo"
CALENDLY_CLIENT_SECRET = "nbnSE4Cgl2pugplOKdXc4Da1qwbkL-TaCsZzsU0Ud0k"
CALENDLY_REDIRECT_URI = "https://the-unseen.onrender.com/calendly/oauth/callback"
# <<< END TEMP >>>


@app.get("/")
def read_root():
    return {"message": "Backend is running"}


@app.get("/calendly/connect")
def calendly_connect():
    authorize_url = (
        "https://auth.calendly.com/oauth/authorize"
        f"?client_id={CALENDLY_CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={CALENDLY_REDIRECT_URI}"
    )
    return {"authorize_url": authorize_url}


@app.get("/calendly/oauth/callback")
async def calendly_callback(code: str):
    """Exchange code for access token (run once)."""
    token_url = "https://auth.calendly.com/oauth/token"

    data = {
        "grant_type": "authorization_code",
        "client_id": CALENDLY_CLIENT_ID,
        "client_secret": CALENDLY_CLIENT_SECRET,
        "redirect_uri": CALENDLY_REDIRECT_URI,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(token_url, data=data)
        return resp.json()
