from fastapi import FastAPI
from app.apis import user, auth, google, posts, comments
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import client, db
from starlette.middleware.sessions import SessionMiddleware
from app.utils.envutils import Environment


env = Environment()

app = FastAPI(title="CONNECTIFY", version="0.1.0")
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


@app.get('/home')
def home():
    return {"message": "You have been logged in through Google OAuth."}


# include routers from routers folder
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(google.router)
app.include_router(posts.router)
app.include_router(comments.router)
