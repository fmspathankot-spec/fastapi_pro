from fastapi import BackgroundTasks,FastAPI,UploadFile,File,Form,HTTPException,status,Depends
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from models import User
import jwt
from authetication import get_password_hash


load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("EMAIL"),
    MAIL_PASSWORD = os.getenv("PASSWORD"),
    MAIL_FROM = os.getenv("EMAIL"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

class EmailSchema(BaseModel):
    email: List[EmailStr]


async def send_email(email: EmailSchema,instance:User):
    toekn_data = {
        "username": instance.username,
        "email": instance.email,
        "password": instance.password
    }
    token = jwt.encode(toekn_data, os.getenv("SECRET_KEY"), algorithm="HS256")
    link = f"http://localhost:8000/verify?token={token}"
    message = MessageSchema(
        subject="Welcome to our platform!",
        recipients=email.email,
        body="Thank you for registering with our platform!",
        type=MessageType.plain
    )


app = FastAPI()

