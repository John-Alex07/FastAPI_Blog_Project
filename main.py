from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from routes.authentication import authentication
from routes.blogs import blogs

app = FastAPI()

app.include_router(authentication)
app.include_router(blogs)
