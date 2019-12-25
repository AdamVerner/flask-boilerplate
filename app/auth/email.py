from flask import render_template, current_app
from app.email import send_email


def send_password_reset_email(email, token):
    send_email(
        f'[{current_app.config.get("APP_NAME")}] reset password',
        sender=current_app.config['ADMINS'][0],
        recipients=[email],
        text_body=render_template('email/reset_password.txt', token=token),
        html_body=render_template('email/reset_password.html', token=token),
    )


def send_registration_token(email, token):
    send_email(
        f'[{current_app.config.get("APP_NAME")}] registration',
        sender=current_app.config.get('MAIL_SENDER'),
        recipients=[email],
        text_body=render_template('email/confirm_registration.txt', token=token),
        html_body=render_template('email/confirm_registration.html', token=token),
    )
