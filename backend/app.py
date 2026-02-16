from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from config import Config
from extensions import db, bcrypt, jwt

from routes.note_routes import note_routes
from routes.auth_routes import auth_routes


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(note_routes)
    app.register_blueprint(auth_routes)

    return app


if __name__ == "__main__":

    app = create_app()

    app.run(host="0.0.0.0", port=8000)