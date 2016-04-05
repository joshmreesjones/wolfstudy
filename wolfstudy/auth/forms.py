from flask.ext.wtf import Form
from wtforms import BooleanField, PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import EqualTo, Length, Required
from wtforms.fields.html5 import EmailField
from ..models import User

class RegisterForm(Form):
    username = StringField('Username', validators=[Required(), Length(min=4, max=30)])
    email = EmailField('Email address', validators=[Required(), Length(min=6, max=320)])
    password = PasswordField('Password', validators=[Required()])
    password_retype = PasswordField('Re-type your password', validators=[Required(), EqualTo('password_retype', message='Passwords must match.')])

    register = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists.')

class LoginForm(Form):
    username = StringField('Username', validators=[Required(), Length(min=4, max=30)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')

    log_in = SubmitField('Log In')

class PasswordResetRequestForm(Form):
    email = EmailField('Email address', validators=[Required(), Length(min=6, max=320)])
    submit = SubmitField('Reset password')

class PasswordResetForm(Form):
    email = EmailField('Email address', validators=[Required(), Length(min=6, max=320)])
    password = PasswordField('Password', validators=[Required(), EqualTo('password_retype', message='Passwords must match.')])
    password_retype = PasswordField('Re-type your password', validators=[Required(), EqualTo('password_retype', message='Passwords must match.')])

    submit = SubmitField('Reset password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')
