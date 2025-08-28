# from fastapi import APIRouter, Cookie, Response, Depends
# from database import get_db
# from models.posting import R_RegistingPosting
# from services.posting import get_posting_preview_list, register_posting, get_posting, change_posting, remove_posting
# from services.security import decode_token
# from time import time

# router = APIRouter(prefix="/posting", tags=["posting"])

# @router.get("/")
# def read_posting(bunch: int = 0, db=Depends(get_db)):
#     if bunch < 0:
#         bunch = 0

#     posting_preview_list = get_posting_preview_list(bunch, db)

#     return posting_preview_list

# @router.post("/")
# def create_posting(posting: R_RegistingPosting, login_token: str | None = Cookie(default=None), db=Depends(get_db)):
#     if login_token is None:
#         return Response(status_code=401)
    
#     login_token = decode_token(login_token)

#     if login_token is None:
#         return Response(status_code=401)
    
#     if login_token["exp"] < time():
#         response = Response(status_code=403)
#         response.delete_cookie("login_token")
#         return response
    
#     user_id = login_token["user_id"]
    
#     posting_id = register_posting(posting, user_id, db)

#     if posting_id is None:
#         return Response(status_code=409)

#     return {"posting_id": posting_id}

# @router.get("/{posting_id}")
# def read_posting(posting_id: int, db=Depends(get_db)):
#     posting = get_posting(posting_id, db)

#     if posting is None:
#         return Response(status_code=404)
    
#     return posting

# @router.put("/{posting_id}")
# def update_posting(posting_id: int, put_data: R_RegistingPosting, login_token: str | None = Cookie(default=None), db=Depends(get_db)):
#     if login_token is None:
#         return Response(status_code=401)
    
#     login_token = decode_token(login_token)

#     if login_token is None:
#         return Response(status_code=401)
    
#     if login_token["exp"] < time():
#         response = Response(status_code=403)
#         response.delete_cookie("login_token")
#         return response
    
#     user_id = login_token["user_id"]

#     try:
#         change_posting(posting_id, put_data, user_id, db)
#         return Response(status_code=200)
#     except Exception as e:
#         raise e
#         return Response(status_code=409)

# @router.delete("/{posting_id}")
# def delete_posting(posting_id: int, login_token: str | None = Cookie(default=None), db=Depends(get_db)):
#     if login_token is None:
#         return Response(status_code=401)
    
#     login_token = decode_token(login_token)

#     if login_token is None:
#         return Response(status_code=401)
    
#     if login_token["exp"] < time():
#         response = Response(status_code=403)
#         response.delete_cookie("login_token")
#         return response
    
#     user_id = login_token["user_id"]
    
#     try:
#         remove_posting(posting_id, user_id, db)
#         return Response(status_code=200)
#     except:
#         return Response(status_code=409)