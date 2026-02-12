
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=200)
    isbn: Optional[str] = Field(default=None, max_length=32)
    published_year: Optional[int] = Field(default=None, ge=0, le=2100)
    copies_total: int = Field(default=1, ge=0)
    copies_available: int = Field(default=1, ge=0)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    author: Optional[str] = Field(default=None, min_length=1, max_length=200)
    isbn: Optional[str] = Field(default=None, max_length=32)
    published_year: Optional[int] = Field(default=None, ge=0, le=2050)
    copies_total: Optional[int] = Field(default=None, ge=0)
    copies_available: Optional[int] = Field(default=None, ge=0)


class BookRead(BookBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MemberBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=50)
    address: Optional[str] = None


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=50)
    address: Optional[str] = None


class MemberRead(MemberBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoanBase(BaseModel):
    book_id: int
    member_id: int


class LoanBorrowRequest(LoanBase):
    due_days: int = Field(default=14, ge=1, le=365)


class LoanReturnRequest(BaseModel):
    loan_id: int


class LoanRead(BaseModel):
    id: int
    book_id: int
    member_id: int
    borrowed_at: datetime
    due_at: Optional[datetime]
    returned_at: Optional[datetime]
    status: str

    model_config = ConfigDict(from_attributes=True)
