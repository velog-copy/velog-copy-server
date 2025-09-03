from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import account, posting, likes, comment, resources
from middleware import exception_catcher

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(exception_catcher)

app.include_router(account.router)
app.include_router(posting.router)
app.include_router(likes.router)
app.include_router(comment.router)
app.include_router(resources.router)