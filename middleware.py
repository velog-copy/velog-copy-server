from fastapi import Request, Response
from jwt.exceptions import ExpiredSignatureError

async def exception_catcher(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except ExpiredSignatureError:
        response = Response(status_code=401)
        response.delete_cookie(key="login", httponly=True)
        return response