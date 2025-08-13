from fastapi import APIRouter, Depends
from database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/")
def read_post_list(bunch: int = 0, db=Depends(get_db)):
    
    return {"message": "hello world", "bunch": bunch}

