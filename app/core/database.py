from pymongo import MongoClient
from ..utils.envutils import Environment

env = Environment()


client = MongoClient(env.MONGO_URI)

db = client["social-media"]

user_collection = db["users"]
