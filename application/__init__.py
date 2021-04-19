import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from application.settings_secrets import *

# Initialize Flask and extensions, such as Flask_SQLAlchemy, Flask_Login, etc.
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'You must be logged in to view that page.'

serializer = URLSafeTimedSerializer(SECRET_KEY)


# Initialize Flask-Mail, used for sending confirmation emails
app.config['MAIL_SERVER'] = 'placeholder'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = MAIL_EMAIL
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_EMAIL
app.config['MAIL_DEBUG'] = True
mail = Mail(app)


# Import each route from all initializations have been finished
from application.routes import account, errors, general
