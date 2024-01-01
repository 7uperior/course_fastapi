from fastapi import FastAPI

app = FastAPI()


@app.
async def first_api():
    return {"message": "Welcome, Vadim!"}
