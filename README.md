
# GitHub Repo Tracker

## Overview

The **GitHub Repo Tracker** is a FastAPI-based backend service that allows you to manage GitHub repositories locally while keeping them in sync with GitHub. It stores repository information in a **PostgreSQL database** and provides RESTful APIs to **create, read, update, and delete repositories**.

The system also integrates with the GitHub API to fetch repository metadata such as stars and forks. This project is designed for scalability, maintainability, and proper error handling.

---

## Features

* Store repository details in PostgreSQL.
* Fetch and update GitHub repository metadata.
* CRUD operations for repositories.
* Proper error handling for database and API operations.
* Fully asynchronous for better performance with `asyncpg` and `httpx`.
* Modular architecture for scalability.

---

## System Design

1. **FastAPI Application** (`main.py`):

   * Entry point for the API.
   * Includes routers and global exception handlers.

2. **Database Layer** (`database.py`):

   * Uses SQLModel with `asyncpg` for asynchronous PostgreSQL interaction.
   * Provides `get_db()` dependency for API endpoints.

3. **Models** (`models.py`):

   * `Repository`: Stores repo name, owner, stars, forks, timestamps.
   * `RepoUpdate`: Stores updates for repositories with timestamps.

4. **API Layer** (`apis/`):

   * `request.py`: Pydantic models for incoming requests.
   * `response.py`: Pydantic models for outgoing responses.
   * `query.py`: CRUD database operations.
   * `routes.py`: FastAPI routers for endpoints.
   * `external_api.py`: Functions to interact with GitHub API.

5. **Utilities** (`utils/exceptions.py`):

   * Custom exceptions and handlers for consistent error responses.

6. **Tests** (`tests/`):

   * Unit tests for database operations.
   * Integration tests for API endpoints.

---

## Database Schema

**PostgreSQL Database:** `github_tracker`

**Tables:**

### repositories

| Column       | Type      | Notes                         |
| ------------ | --------- | ----------------------------- |
| id           | SERIAL    | Primary key                   |
| repo_name    | VARCHAR   | Name of the repository        |
| owner_name   | VARCHAR   | Owner of the repository       |
| stars        | INT       | Default 0                     |
| forks        | INT       | Default 0                     |
| last_updated | TIMESTAMP | Defaults to current timestamp |
| created_at   | TIMESTAMP | Defaults to current timestamp |

### repo_updates

| Column      | Type      | Notes                            |
| ----------- | --------- | -------------------------------- |
| id          | SERIAL    | Primary key                      |
| repo_id     | INT       | Foreign key to `repositories.id` |
| update_type | VARCHAR   | Type of update                   |
| description | TEXT      | Optional description             |
| updated_at  | TIMESTAMP | Defaults to current timestamp    |

---

## API Endpoints

| Method | Endpoint           | Request Body        | Response       | Description                        |
| ------ | ------------------ | ------------------- | -------------- | ---------------------------------- |
| POST   | `/repos`           | `RepoCreate`        | `RepoResponse` | Create repository in GitHub and DB |
| GET    | `/repos/{repo_id}` | None                | `RepoResponse` | Retrieve repository info by ID     |
| PUT    | `/repos/{repo_id}` | `RepoUpdateRequest` | `RepoResponse` | Update repository metadata         |
| DELETE | `/repos/{repo_id}` | None                | `RepoResponse` | Delete repository from DB          |

**Request / Response Models**:

* `RepoCreate`: `repo_name` (str), `owner_name` (str)
* `RepoUpdateRequest`: `stars` (int, optional), `forks` (int, optional)
* `RepoResponse`: `id`, `repo_name`, `owner_name`, `stars`, `forks`, `last_updated`, `created_at`

---

## Error Handling

* 404: Repository not found.
* 500: GitHub API or database operation failed.
* Exceptions are propagated using **FastAPI HTTPException** and custom exception handlers for consistent error messages.

---

## System Scaling

* **Asynchronous operations** for DB and HTTP requests improve performance under high load.
* Modular design allows:

  * Adding new API endpoints easily.
  * Supporting multiple database backends.
* Can be deployed with **Gunicorn + Uvicorn workers** behind a load balancer.
* Horizontal scaling: Multiple instances can run behind a load balancer.
* Caching popular repositories can reduce GitHub API calls.

---

## Setup Instructions

1. **Clone repository**:

```bash
git clone <repo-url>
cd project_root
```

2. **Create virtual environment**:

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / WSL
venv\Scripts\activate      # Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Configure `.env` file**:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost/github_tracker
EXTERNAL_API_URL=https://api.github.com/repos
EXTERNAL_API_TOKEN=<your_github_token>
```

5. **Run PostgreSQL**:

```bash
sudo service postgresql start
psql -U postgres -h localhost -d github_tracker
```

6. **Run the FastAPI app**:

```bash
uvicorn main:app --reload
```

7. **Test endpoints** with **Postman** or **curl**.

---

## Git Ignore

Add the following lines to `.gitignore`:

```
venv/
.env
__pycache__/
*.pyc
```

---

## Usage

1. **Create a repository**:
   POST `/repos` with `repo_name` and `owner_name`.

2. **Read a repository**:
   GET `/repos/{repo_id}`.

3. **Update a repository**:
   PUT `/repos/{repo_id}` with optional `stars` and `forks`.

4. **Delete a repository**:
   DELETE `/repos/{repo_id}`.
