from flask import Flask
from pymongo import MongoClient
from flask_mail import Mail

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # Initialize MongoDB
    mongo = MongoClient(app.config["MONGO_URI"])
    mongo = mongo[app.config["MONGO_DBNAME"]]

    # Initialize Mail
    mail = Mail(app)

    # Register MongoDB and Mail instances with the Flask app
    app.config['MONGO'] = mongo
    app.config['MAIL'] = mail

    # Import and register your routes
    from app.routes import auth_routes, main_routes
    app.register_blueprint(auth_routes)
    app.register_blueprint(main_routes)

    return app
