

# apis/external_api.py
import os
import httpx

GITHUB_TOKEN = os.getenv("EXTERNAL_API_TOKEN")
GITHUB_API_URL =  os.getenv("EXTERNAL_API_URL") # Base URL for creating repos
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

async def fetch_github_repo(owner: str, repo_name: str):
    url = f"https://api.github.com/repos/{owner}/{repo_name}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code != 200:
            return None
        return response.json()

async def create_github_repo(repo_name: str, private: bool = False):
    """
    Creates a new repository under the authenticated user's account.
    """
    url = f"{GITHUB_API_URL}/user/repos"
    payload = {"name": repo_name, "private": private}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=HEADERS)
        if response.status_code not in [200, 201]:
            return None
        return response.json()
