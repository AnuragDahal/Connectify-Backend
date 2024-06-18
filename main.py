from fastapi import FastAPI, HTTPException
from app.apis import user, auth, google, posts, comments, friends
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import client, db
from starlette.middleware.sessions import SessionMiddleware
from app.utils.envutils import Environment
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

env = Environment()

app = FastAPI(title="CONNECTIFY", version="0.1.0")
# Rate limiting middleware
limiter = Limiter(key_func=get_remote_address,
                  default_limits=["1000/hour", "50/minute"])
app.state.limiter = limiter
app.add_exception_handler(HTTPException, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=env.OAUTHSECRET_KEY)

try:
    client.admin.command("ping")
    print("Connected to MongoDB")
except Exception as e:
    print("Failed to connect to MongoDB")
    print(e)


@app.get('/')
def root():
    return {"message": "Welcome to Connectify API, navigate to /docs for documentation."}


@app.get('/home')
def home():
    return {"message": "You have been logged in through Google OAuth."}


# include routers from routers folder
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(google.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(friends.router)
