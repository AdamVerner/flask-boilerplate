from werkzeug.urls import url_parse

from flask import render_template, flash, redirect, url_for, request, send_from_directory, current_app, g
from flask_login import current_user, login_user, logout_user, login_required
import wtforms.validators as validator

from app.errors.handlers import not_found_error
from app.models import User, Admin
from app.main import bp
from app import nav, db


nav.Bar(
    'top',
    [
        nav.Item('Test Page', 'main.testpage'),
        nav.Item('Home', 'main.index'),
    ],
)


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')



@bp.route('/test')
@login_required
def testpage():
    return render_template('test.html')
