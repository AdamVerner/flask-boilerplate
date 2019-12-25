from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return "<Admin {}>".format(self.username)


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)

    username = db.Column(db.String(32))
    email = db.Column(db.String(120))
    password = db.Column(db.String(94))

    def __init__(self, username, email, password):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.confirmed = False

    @staticmethod
    def get(username):
        return User.query.filter((User.username == username) | (User.email == username)).first()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'
                                                 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
