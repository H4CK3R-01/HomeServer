import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import get_db

auth = Blueprint('auth', __name__, static_folder='static', template_folder='templates')


@auth.before_app_request
def load_logged_in_user():
    db = get_db()
    cursor = db.cursor(prepared=True)
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        g.user = cursor.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login_get'))
        return view(**kwargs)
    return wrapped_view


@auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor(prepared=True)
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login_get'))

        flash(error)

    return render_template('register.html')


@auth.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form['user']
    password = request.form['password']
    db = get_db()
    cursor = db.cursor(prepared=True)
    error = None
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user_from_db = cursor.fetchone()
    print(bytes(user_from_db[2]).decode())

    if user_from_db is None:
        error = 'Incorrect username.'
    elif not check_password_hash(bytes(user_from_db[2]).decode(), password):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['user_id'] = user_from_db[0]
        return redirect(url_for('index.start'))

    flash(error)
    return redirect(url_for('auth.login_post'))


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.start'))