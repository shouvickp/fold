from os import environ
class Config:
    MONGODB_SETTINGS = {
        "db": "TheFoldDB",
        "host": environ.get("MONGO_URI", "mongodb://localhost:27017")
    }
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", "super-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = 3600
