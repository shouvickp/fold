from flask import Flask
from flask_cors import CORS
from routes.note_routes import note_routes
from extensions import db
from config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(note_routes)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)