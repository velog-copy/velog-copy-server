from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
import io
from database import get_db
from services.resources import register_image, get_image

router = APIRouter(prefix="/resources", tags=["resources"])

@router.get("/image/{media_id}")
def read_image(media_id: int, db=Depends(get_db)):
    content = get_image(db, media_id)

    return StreamingResponse(io.BytesIO(content), media_type="image/jpeg")


@router.post("/image")
def create_image(file: UploadFile = File(...), db=Depends(get_db)):
    mediaid = register_image(db, file)

    return {"mediaid": mediaid}