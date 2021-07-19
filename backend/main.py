from model import Todo
from database import create_todo, fetch_all_todos, fetch_one_todo, remove_todo, update_todo
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ['http://localhost:3000']

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def read_root():
    return {"Ping": "Pong"}


@app.get("/api/todo")
async def get_todo():
    res = await fetch_all_todos()
    return res


@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_title(title):
    res = await fetch_one_todo(title)
    if res:
        return res
    raise HTTPException(404, f"There is no TODO item with the title {title}")


@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    res = await create_todo(todo.dict())
    if res:
        return res
    raise HTTPException(400, "Something went wrong / Bad Request")


@app.put("/api/todo/{title}", response_model=Todo)
async def put_todo(title: str, desc: str):
    res = await update_todo(title, desc)
    if res:
        return res
    raise HTTPException(404, f"There is no TODO item with the title {title}")


@app.delete("/api/todo/{title}")
async def delete_todo(title):
    res = await remove_todo(title)
    if res:
        return "Successfully deleted the item!"
    raise HTTPException(404, f"There is no TODO item with the title {title}")
