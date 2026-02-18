# Neighborhood Library Service (FastAPI + PostgreSQL)

This is a simple REST service for managing books, members, and lending operations in a small library.

## Features
- Create and update books and members
- Record borrowing and returning books
- List loans (all, by member, or by book)
- Prevent borrowing when no copies are available

## Project Layout
- `app/` FastAPI app and database models, configuration and application logic
- `sql/schema.sql` PostgreSQL schema
- `scripts/client.py` Script To test the flow

## Setup

### 1) Create a database (Docker)

```powershell
# Run PostgreSQL locally
 
 


```

### 2) Create tables

```powershell
# From this repo directory
Get-Content sql/schemas.sql | docker exec -i library-db psql -U postgres -d library
```

### 3) Configure environment

Copy `.env.example` to `.env` and adjust as needed.

### 4) Install dependencies

```powershell
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 5) Run the server

```powershell
uvicorn app.main:app --reload
```

The API will be at `http://127.0.0.1:8000` and Swagger UI at `/docs`.

> **Tip:** if you don't have PostgreSQL available, the app will automatically fall back to using a local `sqlite`
> database (`dev.db` in the project root) on startup. You can run the server without step 1/2 when using the
> fallback, but the Docker/Postgres instructions above are required for production-like behavior.

## Example Requests

```powershell
# Create a book
curl -X POST http://127.0.0.1:8000/books `
  -H "Content-Type: application/json" `
  -d '{"title":"Dune","author":"Frank Herbert","copies_total":2,"copies_available":2}'

# Create a member
curl -X POST http://127.0.0.1:8000/members `
  -H "Content-Type: application/json" `
  -d '{"name":"Member Test","email":"test@example.com"}'

# Borrow a book (book_id=1, member_id=1)
curl -X POST http://127.0.0.1:8000/loans/borrow `
  -H "Content-Type: application/json" `
  -d '{"book_id":1,"member_id":1,"due_days":14}'

# Return a book (loan_id=1)
curl -X POST http://127.0.0.1:8000/loans/return `
  -H "Content-Type: application/json" `
  -d '{"loan_id":1}'

# List loans
curl http://127.0.0.1:8000/loans
```

## Frontend

A minimal React + Vite frontend is included in `frontend/`.
Screenshots of all 3 pages Books, Members and Loans is also added in same location for reference.

Run the frontend:

```powershell
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000`. To change, set `VITE_API_BASE` in the environment.


