from datetime import datetime
from flask import current_app
from flask.ext.login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

MAX_QUESTION_TITLE_LENGTH = 200
MAX_USERNAME_LENGTH = 30
MAX_EMAIL_LENGTH = 320

HASH_ITERATIONS = 2**16
SALT_LENGTH = 64
HASH_LENGTH = 123 # Our current system generates hashes of length 123.

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(MAX_QUESTION_TITLE_LENGTH))
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    answers = db.relationship('Answer', backref='question', lazy='dynamic')

class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(MAX_USERNAME_LENGTH))
    email = db.Column(db.String(MAX_EMAIL_LENGTH), unique=True)
    password_hash = db.Column(db.String(HASH_LENGTH))
    confirmed = db.Column(db.Boolean, default=False)

    questions = db.relationship('Question', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        method = 'pbkdf2:sha1:' + str(HASH_ITERATIONS)
        self.password_hash = generate_password_hash(password, method=method, salt_length=SALT_LENGTH)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
