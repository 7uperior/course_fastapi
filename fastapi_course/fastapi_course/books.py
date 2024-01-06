from fastapi import FastAPI

app = FastAPI()


BOOKS = {
    "book_1": {"title": "title_1", "author": "author_1"},
    "book_2": {"title": "title_2", "author": "author_2"},
    "book_3": {"title": "title_3", "author": "author_3"},
    "book_4": {"title": "title_4", "author": "author_4"},
    "book_5": {"title": "title_5", "author": "author_5"},
}


@app.get("/")
async def read_all_books():
    return BOOKS


@app.get("/books/mybook")
async def read_favorite_book():
    return {"book_title": "My Favorite Book"}


@app.get("/books/{boook_id}")
async def read_book(book_id: int):
    return {"book_titile": book_id}
