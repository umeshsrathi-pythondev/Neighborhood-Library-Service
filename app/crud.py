
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models


# Books

def create_book(db: Session, book: dict) -> models.Book:
    obj = models.Book(**book)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.get(models.Book, book_id)


def list_books(db: Session) -> list[models.Book]:
    return list(db.scalars(select(models.Book).order_by(models.Book.id)).all())


def update_book(db: Session, book_id: int, updates: dict) -> Optional[models.Book]:
    book = get_book(db, book_id)
    if not book:
        return None
    for key, value in updates.items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


# Members

def create_member(db: Session, member: dict) -> models.Member:
    obj = models.Member(**member)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_member(db: Session, member_id: int) -> Optional[models.Member]:
    return db.get(models.Member, member_id)


def list_members(db: Session) -> list[models.Member]:
    return list(db.scalars(select(models.Member).order_by(models.Member.id)).all())


def update_member(db: Session, member_id: int, updates: dict) -> Optional[models.Member]:
    member = get_member(db, member_id)
    if not member:
        return None
    for key, value in updates.items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    return member


# Loans

def borrow_book(db: Session, book_id: int, member_id: int, due_days: int) -> models.Loan:
    book = get_book(db, book_id)
    if not book:
        raise ValueError("Book not found")
    member = get_member(db, member_id)
    if not member:
        raise ValueError("Member not found")
    if book.copies_available <= 0:
        raise ValueError("Book is not available")

    book.copies_available -= 1
    borrowed_at = datetime.now(timezone.utc)
    due_at = borrowed_at + timedelta(days=due_days)

    loan = models.Loan(
        book_id=book_id,
        member_id=member_id,
        borrowed_at=borrowed_at,
        due_at=due_at,
        status="borrowed",
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def return_book(db: Session, loan_id: int) -> models.Loan:
    loan = db.get(models.Loan, loan_id)
    if not loan:
        raise ValueError("Loan not found")
    if loan.status == "returned":
        raise ValueError("Loan already returned")

    book = get_book(db, loan.book_id)
    if not book:
        raise ValueError("Book not found")

    loan.status = "returned"
    loan.returned_at = datetime.now(timezone.utc)
    book.copies_available += 1

    db.commit()
    db.refresh(loan)
    return loan


def list_loans(
    db: Session,
    status: Optional[str] = None,
    member_id: Optional[int] = None,
    book_id: Optional[int] = None,
) -> list[models.Loan]:
    stmt = select(models.Loan).order_by(models.Loan.id)
    if status:
        stmt = stmt.where(models.Loan.status == status)
    if member_id:
        stmt = stmt.where(models.Loan.member_id == member_id)
    if book_id:
        stmt = stmt.where(models.Loan.book_id == book_id)
    return list(db.scalars(stmt).all())
