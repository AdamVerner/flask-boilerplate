import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    APP_NAME = 'Application'

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    MAIL_SENDER = 'webmaster@application.com'

    ADMINS = ['webmaster@apllication.com']

    USE_CAPTCHA = False
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_OPTIONS = {'theme': 'white'}


class TestConfig(object):

    APP_NAME = 'Application - test instance'

    SECRET_KEY = 'testing-is-fun'

    # use temporary sql database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'testapp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TESTING = True
    WTF_CSRF_ENABLED = False

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 8025
    MAIL_USERNAME = 'testing-username'
    MAIL_PASSWORD = 'testing-password'
    MAIL_USE_TLS = None
    MAIL_SENDER = 'webmaster@application.com'


    ADMINS = ['no-reply@testing.com']
