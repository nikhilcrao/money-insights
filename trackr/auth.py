import flask
import functools


from .db import client_context
from .forms import LoginForm, RegistrationForm
from .models import User


from flask import flash, request, redirect, render_template, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


bp = flask.Blueprint('auth', __name__, url_prefix='/auth')


def init_login(login_manager):
    @login_manager.user_loader
    def load_user(username):
        return lookup_user(username)


def lookup_user(username):
    query = User.query(User.username == username)
    with client_context():
        for user in query:
            return user
    return None


def register_user(form):
    username = form['username'].data
    password = form['password'].data

    if lookup_user(username):
        flash('Username already exists.', 'error')
        return None

    user = User(username=username, password=generate_password_hash(password))

    key = None
    with client_context():
        key = user.put()

    if not key:
        flash('Registration error.', 'error')
        return None

    return key


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        if register_user(form):
            return redirect(flask.url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form['username'].data
        password = form['password'].data

        user = lookup_user(username)

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Logged in successfully.')
            return redirect(url_for('index'))

        flash('Login or Password is incorrect.', 'error')

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
