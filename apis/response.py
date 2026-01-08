# apis/response.py
from pydantic import BaseModel
from datetime import datetime

class RepoResponse(BaseModel):
    id: int
    repo_name: str
    owner_name: str
    stars: int
    forks: int
    last_updated: datetime
    created_at: datetime

    class Config:
        orm_mode = True
