from datetime import timedelta
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

# Declare db and sess globally
db = SQLAlchemy()
sess = Session()

def create_app():
    app = Flask(__name__)

    # Import and register blueprints
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    # Session secret key
    app.config['SECRET_KEY'] = 'dev'

    # Assign database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///boxing.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Session config
    app.config["SESSION_PERMANENT"] = True
    app.permanent_session_lifetime = timedelta(days=7)

    # Configure session to be accessed through sqlalchemy
    app.config["SESSION_TYPE"] = "sqlalchemy"
    app.config["SESSION_SQLALCHEMY"] = db


    # Initialize db and sess
    db.init_app(app)
    sess.init_app(app)

    # Create the session table if it doesn't exist
    with app.app_context():
        db.create_all()

    return app
