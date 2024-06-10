from pymongo import MongoClient, IndexModel, ASCENDING
from ..utils.envutils import Environment

env = Environment()


client = MongoClient(env.MONGO_URI)

db = client["social-media"]

user_collection = db["users"]

otp_collection = db["otp"]

post_collection = db["posts"]

comments_collection = db["comments"]


# Create a TTL(Time to live) index on the 'expires_on' field that means after the 30 sec of the value is set for the 'expires_on' field, the document will be deleted.
index = IndexModel([("expires_on", ASCENDING)], expireAfterSeconds=30)
otp_collection.create_indexes([index])
