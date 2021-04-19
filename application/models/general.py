from application import db, login_manager, app
from flask_login import UserMixin


# A requirement of flask-login, let it know how to handle login_user and logout_user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# A user table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # Fields such as email, password, and name
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    confirm = db.Column(db.Boolean, nullable=False, default=False)
