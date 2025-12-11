from fastapi import HTTPException, status
from authetication import get_password_hash, verify_password
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

@post_save(User)
async def create_bussness(
        sender: Type[User],
        instance: User,
        created: bool,
        using_db: Optional[BaseDBAsyncClient] = None,
        update_fields: Optional[List[str]] = None):
    if created:
        bussness_obj = await Bussness.create(
            name=f"{instance.username}'s Business",
            city="Unspecified",
            region="Unspecified",
            user=instance
        )
        await bussness_pydantic.from_tortoise_orm(bussness_obj)


@app.get("/")
def read_root():
    return {"Hello": "World"}

#Register User
@app.post("/register", response_model=user_pydantic_Out)
async def register(user: user_pydantic_In):
    try:
        user_data = user.dict(exclude_unset=True)
        if not all(k in user_data for k in ["username", "email", "password"]):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Missing required fields. Required: username, email, password"
            )

        # Check if user already exists
        if await User.exists(username=user_data["username"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        if await User.exists(email=user_data["email"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user_data["password"] = get_password_hash(user_data["password"])
        user_obj = await User.create(**user_data)
        return await user_pydantic_Out.from_tortoise_orm(user_obj)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid request data: {str(e)}"
        )

#Login User
@app.post("/login", response_model=user_pydantic_Out)
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

