import databases, sqlalchemy, asyncpg
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List


#db
DATABASE_URL = "postgresql://usertest:password@127.0.0.1:5433/dbtest"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "py_users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("gender", sqlalchemy.CHAR),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.CHAR),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

#models
class UserList(BaseModel):
    id: str
    username: str
    password: str
    first_name: str
    last_name: str
    gender: str
    created_at: str
    status: str



app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users", response_model=List[UserList])
async def find_all_users():
    query = users.select()
    return await database.fetch_all(query)