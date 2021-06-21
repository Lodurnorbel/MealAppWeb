import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json, jsonify
)

from flaskr.Models.Services import userService, userRolesService

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = userService.checkForRegister(username, password)

        if error is None:
            userService.create(username, password)
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        error, user = userService.checkForLogin(request.form['username'], request.form['password'])

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect((url_for('index')))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/loginFromOutside', methods=['POST'])
def loginFromOutside():
    result = json.loads(request.get_data().decode("utf-8"))

    msg, _ = userService.checkForLogin(result.get('username'), result.get('password'))
    msg = 'correct' if msg is None else msg

    return jsonify({'msg': msg})


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = userService.getUserById(user_id)
        g.role = userRolesService.getUserRoleByUserId(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

