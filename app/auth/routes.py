from time import time

import jwt
from flask import url_for, redirect, current_app, render_template, request, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.email import send_password_reset_email, send_registration_token
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
from app.auth.forms import ConfirmRegistrationForm
from app.models import User


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """take only email and send jwt to the user to verify him"""

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    if not current_app.config.get('USE_CAPTCHA', False):
        del form.recaptcha

    if form.validate_on_submit():
        token = jwt.encode(
            {
                'email': form.email.data,
                'exp': time() + 600,
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        ).decode("utf-8")

        print(token)

        send_registration_token(form.email.data, token)
        flash('Registration email was sent')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form, use_captcha=current_app.config.get('USE_CAPTCHA', False))


@bp.route('/confirm_registration', methods=['GET', 'POST'])
def confirm_registration():
    """take the jwt and parse the email out"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ConfirmRegistrationForm()

    try:
        decoded = jwt.decode(
            request.args.get('token', ''),
            key=current_app.config.get('SECRET_KEY'),
            algorithms=['HS256']
        )
        form.email.data = decoded.get('email', '')
        form.token.data = request.args.get('token', '')
        form.token.render_kw.update({'readonly': True})
    except jwt.exceptions.ExpiredSignature:
        flash('Token has expired', category='warning')
    except jwt.exceptions.PyJWTError:
        pass

    # the jwt is decoded and validated once again
    if form.validate_on_submit():
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account successfully created')
        return redirect(url_for('.login'))
    return render_template('auth/confirm_registration.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():

    # user is already logged-in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():

        # verify that user is in database
        user = User.get(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            current_app.logger.warning('invalid username/password combo for user %s' % form.username.data)

            return render_template('auth/login.html', form=form, forgotten=True)

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    """log the current user out"""
    current_app.logger.debug(f'user {current_user.username} logged out')
    logout_user()
    flash('successfully logged out')
    return redirect(url_for('main.index'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """
    send an reset password token to the specified email (JWT)
    if user with corresponding email doesn't exist, doesnt send anything.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPasswordRequestForm()

    if not current_app.config.get('USE_CAPTCHA', False):
        del form.recaptcha

    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            token = jwt.encode(
                {
                    'email': form.email.data,
                    'exp': time() + 600,
                },
                current_app.config["SECRET_KEY"],
                algorithm="HS256"
            ).decode("utf-8")
            send_password_reset_email(form.email.data, token)

        flash('Password recovery was sent to your email')
        return redirect(url_for('main.index'))
    return render_template('auth/reset_password_request.html', form=form)


@bp.route('/reset_password/', methods=['GET', 'POST'])
def reset_password():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()

    try:
        decoded = jwt.decode(
            request.args.get('token', ''),
            key=current_app.config.get('SECRET_KEY'),
            algorithms=['HS256'])
        form.email.data = decoded.get('email', '')
        form.token.data = request.args.get('token', '')
        form.token.render_kw.update({'readonly': True})
    except jwt.exceptions.ExpiredSignature:
        flash('Token has expired', category='warning')
    except jwt.exceptions.PyJWTError:
        pass

    # the jwt is decoded and validated once again
    if form.validate_on_submit():
        user = User.get(form.email.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Password successfully changed')
        return redirect(url_for('.login'))
    return render_template('auth/reset_password.html', form=form)

