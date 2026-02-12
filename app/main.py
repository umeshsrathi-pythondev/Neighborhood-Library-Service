
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.db import get_db

app = FastAPI(title="Neighborhood Library Service", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}

# Books

@app.post("/books", response_model=schemas.BookRead, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book.model_dump())


@app.get("/books", response_model=list[schemas.BookRead])
def list_books(db: Session = Depends(get_db)):
    return crud.list_books(db)


@app.get("/books/{book_id}", response_model=schemas.BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=schemas.BookRead)
def update_book(book_id: int, updates: schemas.BookUpdate, db: Session = Depends(get_db)):
    payload = updates.model_dump(exclude_unset=True)
    if not payload:
        raise HTTPException(status_code=400, detail="No fields provided")
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if "copies_total" in payload:
        new_total = payload["copies_total"]
        new_available = payload.get("copies_available", book.copies_available)
        if new_available > new_total:
            raise HTTPException(status_code=400, detail="copies_available cannot exceed copies_total")
    if "copies_available" in payload and "copies_total" not in payload:
        if payload["copies_available"] > book.copies_total:
            raise HTTPException(status_code=400, detail="copies_available cannot exceed copies_total")
    book = crud.update_book(db, book_id, payload)
    return book


# Members

@app.post("/members", response_model=schemas.MemberRead, status_code=201)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    return crud.create_member(db, member.model_dump())


@app.get("/members", response_model=list[schemas.MemberRead])
def list_members(db: Session = Depends(get_db)):
    return crud.list_members(db)


@app.get("/members/{member_id}", response_model=schemas.MemberRead)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = crud.get_member(db, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@app.put("/members/{member_id}", response_model=schemas.MemberRead)
def update_member(member_id: int, updates: schemas.MemberUpdate, db: Session = Depends(get_db)):
    payload = updates.model_dump(exclude_unset=True)
    if not payload:
        raise HTTPException(status_code=400, detail="No fields provided")
    member = crud.update_member(db, member_id, payload)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


# Loans

@app.post("/loans/borrow", response_model=schemas.LoanRead, status_code=201)
def borrow_book(request: schemas.LoanBorrowRequest, db: Session = Depends(get_db)):
    try:
        return crud.borrow_book(db, request.book_id, request.member_id, request.due_days)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/loans/return", response_model=schemas.LoanRead)
def return_book(request: schemas.LoanReturnRequest, db: Session = Depends(get_db)):
    try:
        return crud.return_book(db, request.loan_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/loans", response_model=list[schemas.LoanRead])
def list_loans(
    status: str | None = Query(default=None, pattern="^(borrowed|returned)$"),
    member_id: int | None = None,
    book_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.list_loans(db, status=status, member_id=member_id, book_id=book_id)


@app.get("/members/{member_id}/loans", response_model=list[schemas.LoanRead])
def list_member_loans(member_id: int, db: Session = Depends(get_db)):
    member = crud.get_member(db, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return crud.list_loans(db, member_id=member_id)


@app.get("/books/{book_id}/loans", response_model=list[schemas.LoanRead])
def list_book_loans(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.list_loans(db, book_id=book_id)


# Ensure models are imported so metadata is registered when used elsewhere.
models.Base.metadata
