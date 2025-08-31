from fastapi import APIRouter, Request, Response, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
from database import get_db
from services.resources import process_image, save_image, get_image_tuple, remove_image
import io

router = APIRouter(prefix="/resources", tags=["resources"])

@router.post("/image")
def register_new_image(image_file: UploadFile = File(...), db=Depends(get_db)):
    image_data = process_image(image_file.file)

    if image_data is None:
        return Response(status_code=400)

    image_id = save_image(image_data, db)

    return {"image_id" : image_id}

@router.get("/image/{image_id}")
def return_image_stream(image_id: int, request: Request, db=Depends(get_db)):
    data = get_image_tuple(image_id, db)

    if data is None: return Response(status_code=404)
    if request.headers.get("if-none-match") == str(data.change_id): return Response(status_code=304)

    headers = {
        "ETag": str(data.change_id),
        "Cache-Control": f"public, max-age={24 * 60 * 60 * 30}" # 30일간 캐시
    }

    return StreamingResponse(io.BytesIO(data.image_content), media_type="image/jpeg", headers=headers)

@router.delete("/image/{image_id}")
def delete_image(image_id: int, db=Depends(get_db)):
    try:
        remove_image(image_id, db)
        return Response(status_code=200)
    except:
        return Response(status_code=409)