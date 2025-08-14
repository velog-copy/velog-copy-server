from fastapi import APIRouter, Request, Response, Depends
from database import get_db
from models.posting import R_RegistingPosting
from services.posting import register_posting, get_posting_preview_list, get_posting, remove_posting, change_posting

router = APIRouter(prefix="/posting", tags=["posting"])

@router.post("/")
def create_posting(posting: R_RegistingPosting, db=Depends(get_db)):
    posting_id = register_posting(posting, db)

    return {"posting_id": posting_id}

@router.get("/")
def read_posting(bunch: int = 0, db=Depends(get_db)):
    if bunch < 0:
        bunch = 0

    posting_preview_list = get_posting_preview_list(bunch, db)

    return posting_preview_list
    

@router.get("/{posting_id}")
def read_posting(posting_id: int, db=Depends(get_db)):
    posting = get_posting(posting_id, db)

    if posting is None:
        return Response(status_code=404)
    
    return posting

@router.put("/{posting_id}")
def update_posting(posting_id: int, put_data: R_RegistingPosting, db=Depends(get_db)):
    try:
        change_posting(posting_id, put_data, db)
        return Response(status_code=200)
    except:
        return Response(status_code=409)

@router.delete("/{posting_id}")
def delete_posting(posting_id: int, db=Depends(get_db)):
    try:
        remove_posting(posting_id, db)
        return Response(status_code=200)
    except:
        return Response(status_code=409)