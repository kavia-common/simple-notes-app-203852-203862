from flask import Flask
from flask_cors import CORS
from .routes.health import blp as health_blp
from .routes.notes import blp as notes_blp
from flask_smorest import Api
from .models import db

import os

def make_db_uri():
    # Use SQLite database file in project (notes.db)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    return 'sqlite:///' + os.path.join(base_dir, 'notes.db')

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["API_TITLE"] = "My Flask API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = make_db_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)
api.register_blueprint(health_blp)
api.register_blueprint(notes_blp)
