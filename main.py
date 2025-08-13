from fastapi import FastAPI
from routers import posts, resources

app = FastAPI()

app.include_router(posts.router)
app.include_router(resources.router)