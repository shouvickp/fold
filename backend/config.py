from os import environ
class Config:
    MONGODB_SETTINGS = {
        "db": "TheFoldDB",
        "host": environ.get("MONGO_URI", "mongodb://localhost:27017")
    }