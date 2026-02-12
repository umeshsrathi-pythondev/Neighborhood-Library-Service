
import json
import os
import sys
from typing import Any

import requests


def pretty(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


def main() -> int:
    base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

    print(f"Using API base URL: {base_url}")

    # 1) Create a book
    book_payload = {
        "title": "Title_test",
        "author": "Author_test",
        "copies_total": 2,
        "copies_available": 2,
        "published_year": 2025,
    }
    book = requests.post(f"{base_url}/books", json=book_payload, timeout=10)
    book.raise_for_status()
    book_data = book.json()
    print("Created book:\n", pretty(book_data))

    # 2) Create a member
    member_payload = {"name": "Member test", "email": "membertest@gmail.com"}
    member = requests.post(f"{base_url}/members", json=member_payload, timeout=10)
    member.raise_for_status()
    member_data = member.json()
    print("Created member:\n", pretty(member_data))

    # 3) Borrow the book
    borrow_payload = {
        "book_id": book_data["id"],
        "member_id": member_data["id"],
        "due_days": 14,
    }
    loan = requests.post(f"{base_url}/loans/borrow", json=borrow_payload, timeout=10)
    loan.raise_for_status()
    loan_data = loan.json()
    print("Borrowed:\n", pretty(loan_data))

    # 4) List loans for this member
    loans = requests.get(
        f"{base_url}/members/{member_data['id']}/loans",
        timeout=10,
    )
    loans.raise_for_status()
    print("Member loans:\n", pretty(loans.json()))

    # 5) Return the book
    ret = requests.post(
        f"{base_url}/loans/return",
        json={"loan_id": loan_data["id"]},
        timeout=10,
    )
    ret.raise_for_status()
    print("Returned:\n", pretty(ret.json()))

    return 0


if __name__ == "__main__":
    sys.exit(main())
