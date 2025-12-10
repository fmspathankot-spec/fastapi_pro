from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from tortoise import models
from models import *

#Signals
from tortoise.signals import post_save
from typing import List,Optional,Type
from tortoise import BaseDBAsyncClient

from tortoise import fields
from models import User

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#Register User
@app.post("/register", response_model=user_pydantic)
async def register(user: user_pydantic_In):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] =
    user = await User.create(**user.dict(exclude_unset=True))

    return user_pydantic(user)

#Login User
@app.post("/login", response_model=user_pydantic)
async def login(user: user_pydantic_In):
    user = await User.get(username=user.username)
    return user_pydantic(user)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

