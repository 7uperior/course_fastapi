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


@app.get("/")
async def read_all_books():
    return BOOKS


@app.get("/{book_name}")
async def read_book(book_name: str):
    return BOOKS[book_name]


@app.get("/books/mybook")
async def read_favorite_book():
    return {"book_title": "My Favorite Book"}


# path parameter
@app.get("/books/{boook_id}")
async def read_book_id(book_id: int):
    return {"book_titile": book_id}


@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name, "sub": "Up"}
    if direction_name == DirectionName.south:
        return {"Direction": direction_name, "sub": "Down"}
    if direction_name == DirectionName.east:
        return {"Direction": direction_name, "sub": "Left"}
    return {"Direction": direction_name, "sub": "Right"}
