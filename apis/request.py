# apis/request.py
from pydantic import BaseModel

class RepoCreate(BaseModel):
    repo_name: str
    owner_name: str

class RepoUpdateRequest(BaseModel):
    stars: int | None = None
    forks: int | None = None
