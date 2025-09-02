from fastapi import APIRouter, Depends, Response
from database import get_db
from services.likes import insert_likes, delete_likes, get_likes
from services.account import get_client_info

router = APIRouter(prefix="/likes", tags=["likes"])

@router.get("/")
def search_likes(user_id=Depends(get_client_info), db=Depends(get_db)):
    result = get_likes(user_id, db)
    if result is None:
        return {"likes" : []}
    
    return {"likes" : result}

@router.post("/{posting_id}")
def mark_likes(posting_id: int, user_id=Depends(get_client_info), db=Depends(get_db)):
    if insert_likes(posting_id, user_id, db):
        return Response(status_code=200)
    else:
        return Response(status_code=409)

@router.delete("/{posting_id}")
def unmark_likes(posting_id: int, user_id=Depends(get_client_info), db=Depends(get_db)):
    if delete_likes(posting_id, user_id, db):
        return Response(status_code=200)
    else:
        return Response(status_code=409)