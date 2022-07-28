import logging
from typing import Union
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, status
from app.db import db
from app.schema.secure import UserInDB, User, TokenData, Register, Token
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

SECRET_KEY = "watcharaponweraborirak!@#$61"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate/token")
collection = "secure"

secure = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    user_db = await db.find_one(collection=collection, query={'username': username})
    if user_db:
        return UserInDB(**user_db)
    return None


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        pass
    return user


async def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def register_checking(payload: Register):
    user = await db.find_one(collection=collection,
                             query={'$or': [{'email': payload.email}, {'username': payload.username}]})
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email register already exits.')
    return payload


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


@secure.post('/token')
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@secure.post('/register', response_model=Register)
async def register(payload: Register = Depends(register_checking)):
    password = get_password_hash(payload.hashed_password)
    item_model = jsonable_encoder(payload)
    item_model['hashed_password'] = password
    inserted = await db.insert_one(collection=collection, data=item_model)
    logging.debug(inserted)
    return item_model


@secure.get('/user')
async def get_info(user: dict = Depends(get_current_active_user)):
    return user
