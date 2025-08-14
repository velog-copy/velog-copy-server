from fastapi import FastAPI
from routers import posting, resources

app = FastAPI()

app.include_router(posting.router)
app.include_router(resources.router)