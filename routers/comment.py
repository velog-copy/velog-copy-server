from fastapi import APIRouter, Depends, Response
from database import get_db
from models.comment import commet_DTO
from services.account import get_client_info
from services.comment import make_comment, get_comment_list, delete_comment

router = APIRouter(prefix="/comment")

@router.get("/{posting_id}")
def get_comments(posting_id: int, db=Depends(get_db)):
    return get_comment_list(posting_id, db)

@router.post("/{posting_id}")
def make_new_comment(posting_id: int, comment_content: commet_DTO, user_id=Depends(get_client_info), db=Depends(get_db)):
    comment = comment_content.comment
    comment_id = make_comment(posting_id, user_id, comment, db)
    if not comment_id is None:
        return {"comment_id" : comment_id}
    else:
        return Response(status_code=409)
    

@router.delete("/{posting_id}")
def remove_comment(posting_id: int, user_id=Depends(get_client_info), db=Depends(get_db)):
    if delete_comment(posting_id, user_id, db):
        return Response(status_code=200)
    else:
        return Response(status_code=409)