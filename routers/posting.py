from fastapi import APIRouter, Depends, Response
from database import get_db
from models.posting import J_registering_posting
from services.account import get_client_info
from services.posting import get_posting_list, add_new_posting, get_posting, check_user_have_posting, change_posting, remove_posting

router = APIRouter(prefix="/posting", tags=["posting"])

@router.get("/")
def read_postings(bunch: int, db=Depends(get_db)):
    if bunch < 0:
        bunch = 0

    posting_list = get_posting_list(bunch, db)

    return posting_list

@router.post("/")
def register_posting(posting_content: J_registering_posting, user_id=Depends(get_client_info), db=Depends(get_db)):
    posting_id = add_new_posting(user_id, posting_content, db)

    if posting_id is None:
        return Response(status_code=409)

    return {"posting_id" : posting_id}

@router.get("/{posting_id}")
def read_posting(posting_id: int, db=Depends(get_db)):
    posting_data = get_posting(posting_id, db)
    
    if posting_data is None:
        return Response(status_code=404)

    return posting_data

@router.put("/{posting_id}")
def update_posting(posting_id: int, posting_content: J_registering_posting, user_id=Depends(get_client_info), db=Depends(get_db)):
    if not check_user_have_posting(posting_id, user_id, db):
        return Response(status_code=403)
    
    if change_posting(posting_id, posting_content, db) is None:
        return Response(status_code=409)
    else:
        return Response(status_code=200)

@router.delete("/{posting_id}")
def delete_posting(posting_id: int, user_id=Depends(get_client_info), db=Depends(get_db)):
    if not check_user_have_posting(posting_id, user_id, db):
        return Response(status_code=403)
    
    if remove_posting(posting_id, db) is None:
        return Response(status_code=409)
    else:
        return Response(status_code=200)