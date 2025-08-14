from fastapi import APIRouter, Request, Response, Depends
from database import get_db
from models.posting import R_RegistingPosting
from services.posting import register_posting, get_posting_preview_list, get_posting

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

@router.delete("/{posting_id}")
def read_posting(posting_id: int, db=Depends(get_db)):