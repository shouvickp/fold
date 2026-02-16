from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = MongoEngine()
bcrypt = Bcrypt()
jwt = JWTManager()