from fastapi import APIRouter

router = APIRouter(prefix="posts", tags=["posts"])

@router.get("/")
def read_post_list(bunch: int = 0):
    return {"message": "hello world", "bunch": bunch}

