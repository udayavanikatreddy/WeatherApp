from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

# Enable CORS for all routes
CORS(app)

# Ensure the tables are created before running the app
with app.app_context():
    db.create_all()
