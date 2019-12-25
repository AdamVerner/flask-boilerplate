import os
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_navigation import Navigation
from flask_dotenv import DotEnv


from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "Please log in to access this page."
mail = Mail()
migrate = Migrate()
nav = Navigation()
env = DotEnv()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    env.init_app(app, env_file='.flaskenv', verbose_mode=True)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    nav.init_app(app)

    from app.main import bp as main_bp
    from app.errors import bp as errors_bp
    from app.api import bp as api_bp
    from app.auth import bp as auth_bp



    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp, url_prefix="/error")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    if not app.config["MAIL_SERVER"]:
        raise Exception('Mail server must be set')

    auth = None
    if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
        auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
    secure = None
    if app.config["MAIL_USE_TLS"]:
        secure = ()
    mail_handler = SMTPHandler(
        mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
        fromaddr="no-reply@" + app.config["MAIL_SERVER"],
        toaddrs=app.config["ADMINS"],
        subject="Application Failure",
        credentials=auth,
        secure=secure,
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler("logs/application.log", maxBytes=10240, backupCount=10)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.DEBUG)
    app.logger.info("application startup")

    return app


from app import models, errors
