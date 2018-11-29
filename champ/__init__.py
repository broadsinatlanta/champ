from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from champ.personal import secret_key
from champ.helper import exerciseData

# Initialise app
app = Flask(__name__)
data = exerciseData()

# Secret key for form
app.config["SECRET_KEY"] = secret_key

# Config database
app.config["SQLAlCHEYMY_DATABASE_URI"] = "sqlite:///champ.db"
db = SQLAlchemy(app)


# Create all tables on first request
@app.before_first_request
def make_tables():
    """
    Make tables to insert feedback.
    """
    from champ.models import Feedback
    db.create_all()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

from champ import routes
