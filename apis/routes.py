# apis/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .request import RepoCreate, RepoUpdateRequest
from .response import RepoResponse
from .query import create_repo, get_repo, update_repo, delete_repo
from .external_api import fetch_github_repo
router = APIRouter()



from .external_api import fetch_github_repo, create_github_repo

@router.post("/repos", response_model=RepoResponse, status_code=201)
async def add_repo(repo: RepoCreate, db: AsyncSession = Depends(get_db)):
    try:
        # 1️⃣ Create repo on GitHub
        github_data = await create_github_repo(repo.repo_name)
        if github_data is None:
            raise HTTPException(status_code=500, detail="Failed to create repo on GitHub")

        stars = github_data.get("stargazers_count", 0)
        forks = github_data.get("forks_count", 0)

        # 2️⃣ Save repo to DB
        return await create_repo(db, repo.repo_name, repo.owner_name, stars=stars, forks=forks)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create repository: {str(e)}")

@router.get("/repos/{repo_id}", response_model=RepoResponse)
async def read_repo(repo_id: int, db: AsyncSession = Depends(get_db)):
    try:
        repo = await get_repo(db, repo_id)
        if not repo:
            raise HTTPException(status_code=404, detail="Repository not found")
        return repo
    except HTTPException:  # propagate 404
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch repository: {str(e)}")

@router.put("/repos/{repo_id}", response_model=RepoResponse)
async def modify_repo(repo_id: int, repo_update: RepoUpdateRequest, db: AsyncSession = Depends(get_db)):
    try:
        repo = await update_repo(db, repo_id, stars=repo_update.stars, forks=repo_update.forks)
        if not repo:
            raise HTTPException(status_code=404, detail="Repository not found")
        return repo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update repository: {str(e)}")

@router.delete("/repos/{repo_id}", response_model=RepoResponse)
async def remove_repo(repo_id: int, db: AsyncSession = Depends(get_db)):
    try:
        repo = await delete_repo(db, repo_id)
        if not repo:
            raise HTTPException(status_code=404, detail="Repository not found")
        return repo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete repository: {str(e)}")
