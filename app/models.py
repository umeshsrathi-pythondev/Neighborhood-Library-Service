from __future__ import annotations

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Book(Base):
    """
    Book class with title, author, publication info, and inventory tracking for total and available copies
    """
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author: Mapped[str] = mapped_column(String(200), nullable=False)
    isbn: Mapped[str | None] = mapped_column(String(32), unique=True)
    published_year: Mapped[int | None] = mapped_column(Integer)
    copies_total: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    copies_available: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    loans: Mapped[list[Loan]] = relationship(back_populates="book")

    __table_args__ = (
        CheckConstraint("copies_total >= 0", name="ck_books_copies_total"),
        CheckConstraint("copies_available >= 0", name="ck_books_copies_available"),
        CheckConstraint("copies_available <= copies_total", name="ck_books_copies_available_le_total"),
    )


class Member(Base):
    """
    Membership records for library users, with contact info and book borrow history
    """
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(String(200), unique=True)
    phone: Mapped[str | None] = mapped_column(String(50))
    address: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    loans: Mapped[list[Loan]] = relationship(back_populates="member")


class Loan(Base):
    """Loan term for borrowed books, with status tracking and due dates
    """
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="RESTRICT"), nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="RESTRICT"), nullable=False)
    borrowed_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    due_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    returned_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="borrowed")

    book: Mapped[Book] = relationship(back_populates="loans")
    member: Mapped[Member] = relationship(back_populates="loans")

    __table_args__ = (
        CheckConstraint("status in ('borrowed','returned')", name="ck_loans_status"),
    )
