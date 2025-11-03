from flask import Flask
from flask_cors import CORS
from routes.note_routes import note_routes
from extensions import db
from config import Config
from os import environ
from dotenv import load_dotenv

load_dotenv() 

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    print(app.config['MONGODB_SETTINGS'])
    db.init_app(app)
    app.register_blueprint(note_routes)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=environ.get("PORT", 5000), debug=True)