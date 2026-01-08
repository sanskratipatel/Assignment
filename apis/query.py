# apis/query.py
from models import Repository 
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

async def create_repo(db: AsyncSession, repo_name: str, owner_name: str, stars: int = 0, forks: int = 0):
    repo = Repository(repo_name=repo_name, owner_name=owner_name, stars=stars, forks=forks)
    db.add(repo)
    await db.commit()
    await db.refresh(repo)
    return repo


async def get_repo(db: AsyncSession, repo_id: int):
    result = await db.execute(select(Repository).where(Repository.id == repo_id))
    return result.scalar_one_or_none()

async def update_repo(db: AsyncSession, repo_id: int, stars: int | None = None, forks: int | None = None):
    repo = await get_repo(db, repo_id)
    if not repo:
        return None
    if stars is not None:
        repo.stars = stars
    if forks is not None:
        repo.forks = forks
    await db.commit()
    await db.refresh(repo)
    return repo

async def delete_repo(db: AsyncSession, repo_id: int):
    repo = await get_repo(db, repo_id)
    if not repo:
        return None
    await db.delete(repo)
    await db.commit()
    return repo
