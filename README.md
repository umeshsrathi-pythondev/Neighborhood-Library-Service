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
 docker run --name library-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=library -p 5432:5432 -d postgres:16
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


