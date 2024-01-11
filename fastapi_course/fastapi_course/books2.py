from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(
        default=None,
        title="Description of the book",
        min_length=1,
        max_length=100,
    )
    rating: int = Field(gt=-1, lt=101)

    class Config:
        json_schema_extra = {
            "example": {
                "id": uuid4(),
                "title": "Vadim is the Best PRO Python Programmer",
                "author": "Vadim Surin",
                "description": "Vadim will do all the things needed to be a PRO Python Coder",
                "rating": 100,
            }
        }


BOOKS = []


@app.get("/")
async def read_all_books():
    if len(BOOKS) < 1:
        create_books_no_api()
    return BOOKS


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


def create_books_no_api():
    book_1 = Book(
        id=uuid4(),
        title="Title 1",
        author="Author 1",
        description="Description 1",
        rating=60,
    )
    book_2 = Book(
        id=uuid4(),
        title="Title 2",
        author="Author 2",
        description="Description 2",
        rating=70,
    )
    book_3 = Book(
        id=uuid4(),
        title="Title 3",
        author="Author 3",
        description="Description 3",
        rating=80,
    )
    book_4 = Book(
        id=uuid4(),
        title="Title 4",
        author="Author 4",
        description="Description 4",
        rating=90,
    )
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
