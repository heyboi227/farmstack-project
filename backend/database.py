from model import Todo
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
database = client['TodoList']
myCollection = database['Todo']


async def fetch_one_todo(title):
    document = myCollection.find_one({"title": title})
    return document


async def fetch_all_todos():
    todos = []
    cursor = myCollection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos


async def create_todo(todo):
    document = todo
    result = await myCollection.insert_one(document)
    return result


async def update_todo(title, desc):
    await myCollection.update_one({"title": title}, {"$set": {"description": desc}})
    document = await myCollection.find_one({"title": title})
    return document


async def remove_todo(title):
    await myCollection.delete_one({"title": title})
    return True
