# utils/exceptions.py
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status

class RepoNotFoundException(Exception):
    pass

async def repo_exception_handler(request: Request, exc: RepoNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)}
    )
