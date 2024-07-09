import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Optional
from models import TokenData

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

class User:
    def __init__(self, username: str, password: str, role: str):
        self.username = username
        self.password = password
        self.role = role

class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, username: str, password: str, role: str):
        if username in self.users:
            raise ValueError("User already exists")
        hashed_password = get_password_hash(password)
        self.users[username] = User(username, hashed_password, role)

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.users.get(username)
        if user and verify_password(password, user.password):
            return user
        return None

    def get_user(self, username: str) -> Optional[User]:
        return self.users.get(username)

user_manager = UserManager()

# Add a default admin user
try:
    user_manager.add_user("admin", "adminpassword", "administrator")
except ValueError:
    pass

def get_current_user(token: str = Depends(oauth2_scheme)):
    print(f"Received token: {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            print(11111111)
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        print(111)
        raise credentials_exception
    user = user_manager.get_user(username=token_data.username)
    if user is None:
        print(222)
        raise credentials_exception
    print(f"Decoded token payload: {payload}")
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return current_user
