from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from models.user import User, UserInDB, UserCreate, UserUpdate
from config.database import db
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

authentication = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to get user by username
async def get_user_by_username(username: str):
    user = await db["Users"].find_one({"username": username})
    return user

# Function to authenticate user
async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user

# Function to get current user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print(token)
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user

# Route to register a new user
@authentication.post("/register", response_model=User)
async def register_user(user: UserCreate):
    user_dict = user.dict()
    user_dict["password"] = pwd_context.hash(user.password)
    user_dict["created_at"] = datetime.now()
    user_dict["tags"] = user.tags
    user_id = await db["Users"].insert_one(user_dict)
    created_user = await db["Users"].find_one({"_id": user_id.inserted_id})
    return created_user

# Route to generate access token
@authentication.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Route to authenticate user and generate access token
@authentication.post("/login")
async def login_user(username: str, password: str):
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Route to update user profile
@authentication.put("/profile", response_model=User)
async def update_profile(user: UserUpdate, current_user: User = Depends(get_current_user)):
    await db["Users"].update_one({"username": current_user["username"]}, {"$set": user.dict()})
    updated_user = await db["Users"].find_one({"username": current_user["username"]})
    return updated_user

# Route to add tags to user profile
@authentication.post("/tags/add", response_model=User)
async def add_tags(tags: list[str], current_user: User = Depends(get_current_user)):
    await db["Users"].update_one({"username": current_user["username"]}, {"$addToSet": {"tags": {"$each": tags}}})
    updated_user = await db["Users"].find_one({"username": current_user["username"]})
    return updated_user

# Route to remove tags from user profile
@authentication.post("/tags/remove", response_model=User)
async def remove_tags(tags: list[str], current_user: User = Depends(get_current_user)):
    await db["Users"].update_one({"username": current_user["username"]}, {"$pullAll": {"tags": tags}})
    updated_user = await db["Users"].find_one({"username": current_user["username"]})
    return updated_user
