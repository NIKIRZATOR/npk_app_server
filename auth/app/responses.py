from fastapi import HTTPException

def ok(body=None, message: str = "ok"):
    return {"status": "ok", "message": message, "data": body}

def bad_request(message: str):
    raise HTTPException(status_code=400, detail=message)

def unauthorized(message: str):
    raise HTTPException(status_code=401, detail=message)

def forbidden(message: str):
    raise HTTPException(status_code=403, detail=message)

def not_found(message: str):
    raise HTTPException(status_code=404, detail=message)
