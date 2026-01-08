# main.py
from fastapi import FastAPI
from apis.routes import router as repo_router
from utils.exceptions import repo_exception_handler, RepoNotFoundException

app = FastAPI(title="GitHub Repo Tracker")

app.include_router(repo_router)

# Global exception
app.add_exception_handler(RepoNotFoundException, repo_exception_handler)
