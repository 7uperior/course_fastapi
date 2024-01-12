from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


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
                "description": "Vadim will be a PRO Python Coder",
                "rating": 100,
            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: Optional[str] = Field(
        default=None,
        title="Description of the book",
        min_length=1,
        max_length=100,
    )


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(
    request: Request, exc: NegativeNumberException
):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Hey, why do you want {exc.books_to_return} "
            f"books? You need to reed more!"
        },
    )


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(BOOKS) < 1:
        create_books_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.get("/books/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f"book with ID: {book_id} deleted"
    raise raise_item_cannot_be_found_exception()


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


def raise_item_cannot_be_found_exception():
    return HTTPException(
        status_code=404,
        detail="Book not found",
        headers={"X-Header_Error": "Nothing to be seen at UUID"},
    )
