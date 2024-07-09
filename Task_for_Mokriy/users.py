from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models import UserIn, Token
from auth import user_manager, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
import asyncio
router = APIRouter()

@router.post("/register", response_model=UserIn)
async def register(user: UserIn):
    print(11111111)
    try:
        user_manager.add_user(user.username, user.password, user.role)
    except ValueError:
        raise HTTPException(status_code=400, detail="User already exists")
    return user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_manager.authenticate(form_data.username, form_data.password)
    if not user:
        await asyncio.to_thread(print, 1111)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    await asyncio.to_thread(print, access_token)
    return {"access_token": access_token, "token_type": "bearer"}
