from datetime import datetime, timedelta
from random import shuffle
from typing import List, Union
import os

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

import yamldb
from users import Users, UserWithPassword, User, EditableUser
import sss

SECRET_KEY = os.environ.get("SECRET_KEY", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

db = yamldb.Db("./users.yaml")
users = Users(db, pwd_context)

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    global users
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = users.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/api/token", response_model=Token, tags=["auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    global users
    user = users.authenticate(form_data.username, form_data.password)
    if not user:
        # Sign up if not exists
        user = UserWithPassword(username=form_data.username, password=form_data.password)
        print(f"REG: {user}")
        try:
            users.insert_or_update(user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        print(f"LOGIN: {user}")
    if ACCESS_TOKEN_EXPIRE_MINUTES:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        access_token_expires = None
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/me", response_model=User, tags=["user"])
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/api/me", response_model=User, tags=["user"])
async def edit_profile(user: EditableUser, current_user: User = Depends(get_current_user)):
    u = dict(current_user)
    u.update(dict(user))
    print(f"EDIT: {u}")

    return users.insert_or_update(User(**u))

@app.get("/api")
def read_root():
    return "phone API v1"

class ContactBook(BaseModel):
    contacts: List[User]

@app.get("/api/admin", response_model=ContactBook, tags=["admin"])
def read_admin_data(current_user: User = Depends(get_current_user)):
    if current_user.level < 1337:
        raise  HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Your level is less than 1337",
        )

    signature = sss.sign(dict(current_user))
    if signature != db.data[current_user.username].get("signature"):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid signature"
        )

    all_users = [User(username=key, **val) for key, val in db.data.items()]
    all_users.append(User(
        username="secret_contact",
        name="secret contact",
        phone=sss.FLAG,
        level=31337))
    shuffle(all_users)
    book = ContactBook(contacts=all_users)
    print(f"BOOK: {current_user}")
    return book