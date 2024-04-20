import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('system', __name__, url_prefix='/system')

@bp.route('/index', methods=('GET', 'POST'))
def index():
    stream = {'is_online':'super'}
    g.user = { 'page_num':1, 'count':1, 
                'pageLabels':[{'cur':1, 'name':'name'}, {'cur':2, 'name':'name2'}]}
    g.pageData = { 'page_num':1, 'count':1, 
                'pageLabels':[{'cur':1, 'name':'name'}, {'cur':2, 'name':'name2'}]}
    return render_template('app/web_system_index.html')

@bp.route('/settings', methods=('GET', 'POST'))
def settings():
    stream = {'is_online':'super'}
    g.obj = { 'page_num':1, 'count':1, 
                'pageLabels':[{'cur':1, 'name':'name'}, {'cur':2, 'name':'name2'}]}
    g.pageData = { 'page_num':1, 'count':1, 
                'pageLabels':[{'cur':1, 'name':'name'}, {'cur':2, 'name':'name2'}]}
    return render_template('app/web_system_settings.html')
    
@bp.route('/auth', methods=('GET', 'POST'))
def auth():
    stream = {'is_online':'super'}
    g.obj = { 'page_num':1, 'count':1, 
                'pageLabels':[{'cur':1, 'name':'name'}, {'cur':2, 'name':'name2'}]}
    g.settings = { 'page_num':1, 'count':1, 
                'pageLabels':[{'cur':1, 'name':'name'}, {'cur':2, 'name':'name2'}]}
    return render_template('app/web_system_auth.html')

@bp.route('/getHandle', methods=('GET', 'POST'))
def get_handle():
    stream = {'is_online':'super'}
    return stream
    

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
    print('ok')
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

    return render_template('app/web_index.html')
    
@bp.route('/getIndex', methods=('GET', 'POST'))
def get_index():
    res = {'data':[{'process_name':'Admin', 'state':1, 'spend_date_str':222},{}]}
    return res
    
@bp.route('/getAuth', methods=('GET', 'POST'))
def get_auth():
    res = {'info':{'state':'1', 'dongle_status':1, 'expire_hour':222, 'remark':'remark', 'create_date_str':'create_date_str', 'expire_date_str':'expire_date_str'}}
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