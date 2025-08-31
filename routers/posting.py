from fastapi import APIRouter, Depends
from database import get_db
from services.account import get_client_info

router = APIRouter(prefix="/posting", tags=["posting"])

@router.get("/")
def read_postings():
    pass

@router.post("/")
def create_posting():
    pass

@router.get("/{posting_id}")
def read_posting():
    pass

@router.put("/{posting_id}")
def update_posting():
    pass

@router.delete("/{posting_id}")
def delete_posting():
    pass