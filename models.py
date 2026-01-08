# models.py
from sqlmodel import SQLModel, Field
from datetime import datetime
class Repository(SQLModel, table=True):
    __tablename__ = "repositories"  # match DB
    id: int = Field(default=None, primary_key=True)
    repo_name: str
    owner_name: str
    stars: int = 0
    forks: int = 0
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RepoUpdate(SQLModel, table=True):
    __tablename__ = "repo_updates"
    id: int = Field(default=None, primary_key=True)
    repo_id: int = Field(foreign_key="repositories.id")  # also match plural
    update_type: str
    description: str | None = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
