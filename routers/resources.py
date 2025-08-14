from fastapi import APIRouter, Request, Response, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
import io
from database import get_db
from services.resources import register_image, get_image
from models.resources import T_image

router = APIRouter(prefix="/resources", tags=["resources"])

@router.get("/image/{image_id}")
def read_image(image_id: int, request: Request, db=Depends(get_db)):
    data: T_image | None = get_image(image_id, db)

    if data is None:
        return Response(status_code=404)

    if request.headers.get("if-none-match") == str(data.change_id):
        return Response(status_code=304)

    headers = {
        "ETag": str(data.change_id),
        "Cache-Control": "public, max-age=31536000"
    }

    return StreamingResponse(io.BytesIO(data.image_data), media_type="image/jpeg", headers=headers)


@router.post("/image")
def create_image(file: UploadFile = File(...), db=Depends(get_db)):
    image_id = register_image(file.file, db)

    if image_id is None:
        return Response(status_code=415)

    return {"image_id": image_id}