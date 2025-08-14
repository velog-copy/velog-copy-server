from fastapi import APIRouter, Request, Response, Depends
from database import get_db
from models.posting import R_posting
from services.posting import register_posting

router = APIRouter(prefix="/posting", tags=["posting"])

@router.post("/")
def create_posting(posting: R_posting, db=Depends(get_db)):
    posting_id = register_posting(posting, db)
    
    return {"posting_id": posting_id}

