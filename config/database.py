from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# MongoDB connection
MONGODB_URL = "mongodb+srv://admin:admin@demo.d6mozcq.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGODB_URL)
db = AsyncIOMotorDatabase(client, "Blog_Base")

# client = MongoClient(MONGODB_URL)
# db = client["Blog_Base"]