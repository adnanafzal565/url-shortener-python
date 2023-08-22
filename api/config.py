from fastapi import FastAPI
app = FastAPI()
auth_app = FastAPI()
from pymongo import MongoClient

jwt_secret = "qwertyuiopasdfgfhjklzxcvbnm"

MONGO_CONNECTING_STRING = "mongodb://localhost:27017"
client = MongoClient(MONGO_CONNECTING_STRING)
db_name = "url_shortener"
db = client[db_name]