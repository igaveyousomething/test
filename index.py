import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from .utils.OSInfo import OSInfo

bp = Blueprint('index', __name__, url_prefix='/index')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')
    
@bp.route('/login', methods=('GET', 'POST'))
def login():
    settings = {'name':'视频行为分析系统', 'welcome':'welcome', 'logo_url':'/static/images/user.png', 
                'bottom_name':'bottom_name', 'is_show_author':1, 'author_link':'link', 
                'author':'author'}
    session['settings'] = settings
    g.settings = settings
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('app/web_login.html')
    
@bp.route('/main', methods=('GET', 'POST'))
def main():
    settings = {'name':'视频行为分析系统', 'welcome':'welcome', 'logo_url':'/static/images/user.png', 
                'bottom_name':'bottom_name', 'is_show_author':1, 'author_link':'link', 
                'author':'author'}
    session['settings'] = settings
    
    g.settings = settings
    return render_template('app/web_index.html')
    
@bp.route('/getIndex', methods=('GET', 'POST'))
def get_index():
    try:
        osSystem = OSInfo()
        os_info = osSystem.info()
        code = 1000
        msg = "success"

    except Exception as e:
        msg = str(e)

    res = {
        "code":code,
        "msg":msg,
        "osInfo":os_info
    }
    print(res)
    return res
    
@bp.route('/getAuth', methods=('GET', 'POST'))
def get_auth():
    code = 0
    msg = "error"
    os_info = {}
    try:
        osSystem = OSInfo()
        os_info = osSystem.info()
        code = 1000
        msg = "success"

    except Exception as e:
        msg = str(e)

    res = {
        "code":code,
        "msg":msg,
        "os_info":os_info
    }
    print(res)
    return res
    
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
        
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