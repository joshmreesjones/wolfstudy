from flask.ext.login import UserMixin
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

    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __init__(self, title, content):
        self.title = title
        self.content = content

class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, content, question):
        self.content = content
        self.question_id = question.id
        self.question = question

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(MAX_USERNAME_LENGTH))
    email = db.Column(db.String(MAX_EMAIL_LENGTH), unique=True)
    password_hash = db.Column(db.String(HASH_LENGTH))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email

        method = 'pbkdf2:sha1:' + str(HASH_ITERATIONS)
        self.password_hash = generate_password_hash(password, method=method, salt_length=SALT_LENGTH)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
