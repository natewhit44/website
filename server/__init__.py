from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from server.config import Config

# Initialize DB
db = SQLAlchemy()

# Initialize password encryption
bcrypt = Bcrypt()

# Initialize login
login_manager = LoginManager()

# Set login routes
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# Initialize mail server
mail = Mail()

# Function to create app instance
def create_app(config_class=Config):
    # Initialize app
    app = Flask(__name__)

    # Set app configuration
    app.config.from_object(Config)

    # Run init method for flask extensions used in app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Import blueprint objects
    from server.users.routes import users
    from server.posts.routes import posts
    from server.main.routes import main
    from server.errors.handlers import errors

    # Register blueprints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app