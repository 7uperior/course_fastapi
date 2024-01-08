from typing import Optional
from fastapi import FastAPI
from enum import Enum


app = FastAPI()


BOOKS = {
    "book_1": {"title": "title_1", "author": "author_1"},
    "book_2": {"title": "title_2", "author": "author_2"},
    "book_3": {"title": "title_3", "author": "author_3"},
    "book_4": {"title": "title_4", "author": "author_4"},
    "book_5": {"title": "title_5", "author": "author_5"},
}


class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"


# @app.get("/")
# async def read_all_books():
#     return BOOKS


# Optional query - we can delite, but we can also don't delite the item (book)
# skip 1 book
@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS


@app.get("/{book_name}")
async def read_book(book_name: str):
    return BOOKS[book_name]


# 1. Create a new read book function that
# uses query params instead of path params
@app.get("/assignment/")
async def read_book_query(book_name: Optional[str] = None):
    if book_name:
        return BOOKS[book_name]
    return "No books have been choosen"


@app.post("/")
async def create_book(book_title, book_author):
    current_book_id = 0

    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split("_")[-1])
            print(x)
            if x > current_book_id:
                current_book_id = x
    BOOKS[f"book_{current_book_id+1}"] = {
        "title": book_title,
        "author": book_author,
    }
    return BOOKS[f"book_{current_book_id+1}"]


@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    book_information = {"title": book_title, "author": book_author}
    BOOKS[book_name] = book_information
    return book_information


@app.delete("/{book_name}")
async def delete_book(book_name: str):
    del BOOKS[book_name]
    return f"Book {book_name} deleted"


# 2. Create a new delete book function that
# uses query params instead of path params
@app.delete("/assignment/")
async def delete_book_query(book_name: Optional[str] = None):
    if book_name:
        del BOOKS[book_name]
        return f"Book {book_name} deleted with query params"
    return "No books have been deleted"


@app.get("/books/mybook")
async def read_favorite_book():
    return {"book_title": "My Favorite Book"}


# path parameter
@app.get("/books/{boook_id}")
async def read_book_id(book_id: int):
    return {"book_title": book_id}


@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name, "sub": "Up"}
    if direction_name == DirectionName.south:
        return {"Direction": direction_name, "sub": "Down"}
    if direction_name == DirectionName.east:
        return {"Direction": direction_name, "sub": "Left"}
    return {"Direction": direction_name, "sub": "Right"}
