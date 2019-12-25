import jwt
from flask import current_app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms import FieldList, FormField, Form, HiddenField
import wtforms.validators as validator

from app.models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[validator.DataRequired(), validator.Email()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise validator.ValidationError('Email already taken')


class ConfirmRegistrationForm(FlaskForm):
    token = StringField('Token', default='', render_kw={})
    email = StringField('email', default='', render_kw={'readonly': True})
    username = StringField('Username', validators=[validator.DataRequired(), validator.length(4, 32)])
    password = PasswordField('Password', validators=[validator.DataRequired(), validator.length(8)])
    password2 = PasswordField('Repeat Password', validators=[validator.DataRequired(), validator.EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise validator.ValidationError('Username already taken')

    def validate_token(self, token):
        try:
            jwt.decode(
                token.data,
                key=current_app.config.get('SECRET_KEY'),
                algorithms=['HS256']
            )
        except jwt.exceptions.ExpiredSignature:
            current_app.logger.debug('JWT has expired')
            raise validator.ValidationError("Token has expired")
        except jwt.exceptions.PyJWTError:
            current_app.logger.debug('failed to decode JWT')
            raise validator.ValidationError('Invalid token')

    def validate_email(self, email):
        try:
            token = jwt.decode(
                self.token.data,
                key=current_app.config.get('SECRET_KEY'),
                algorithms=['HS256']
            )
            token_mail = token.get('email', None)
            if not token_mail:
                current_app.logger.debug('No email in jwt token')
                raise validator.ValidationError('Invalid token')
            if email.data != token_mail:
                current_app.logger.debug('JWT email does not match form email')
                raise validator.ValidationError('Invalid token')
        except jwt.exceptions.PyJWTError:
            current_app.logger.debug('failed to decode JWT')
            raise validator.ValidationError('Invalid token')

        if User.query.filter_by(email=email.data).first():
            current_app.logger.debug('Email is already registered')
            raise validator.ValidationError('Email is already registered')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validator.DataRequired()])
    password = PasswordField('Password', validators=[validator.DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[validator.DataRequired(), validator.Email()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    token = StringField('Token', default='', render_kw={})
    email = StringField('email', default='', render_kw={'readonly': True})

    validate_token = ConfirmRegistrationForm.validate_token

    password = PasswordField('Password', validators=[validator.DataRequired(), validator.length(8)])
    password2 = PasswordField('Repeat Password', validators=[validator.DataRequired(), validator.EqualTo('password')])
    submit = SubmitField('Request Password Reset')


