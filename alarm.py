import functools
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db, query_db, insert_db, delete_db, update_db
from .utils.Utils import buildPageLabels, gen_code

bp = Blueprint('alarm', __name__, url_prefix='/alarm')

@bp.route('/index', methods=('GET', 'POST'))
def index():
    data = []
    for item in query_db("SELECT * FROM av_alarm"):
        data.append(dict(item))
    g.pageData = { 'page_num':1, 'count':len(data), 'page_size':1,
                'pageLabels':buildPageLabels(1, 1)}
    return render_template('alarm/index.html')
    
@bp.route('/show', methods=('GET', 'POST'))
def show():
    g.alarm = {'flag':1, 'code': 1, 'create_time':'20240101', 'video_count':1, 'image_count':5, 'imageUrlArray':['url1', 'url2'],
                'control_code':1, 'imageUrl':'url', 'videoUrl':'url'}
                
    g.alarm_related_data = [{'draw_type':1, 'create_time':'20240101', 'code':2}]
    return render_template('alarm/show.html')
    
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
    res = {'osInfo':[{'os_cpu_used_rate':20, 'os_virtual_mem_used_rate':1, 'os_disk_used_rate':22,
            'os_cpu_used_rate_str':22, 'os_virtual_mem_used_rate_str':23, 
            'os_disk_used_rate_str':23, 'os_run_date_str':23, }]}
            
    data = []
    for item in query_db("SELECT *, create_time as create_time_str FROM av_alarm"):
        data.append(dict(item))
    pageData = { 'page_num':1, 'count':len(data), 'page_size':1,
                'pageLabels':buildPageLabels(1, 1)}
    res = {'code':1000, 'data':data, 'pageData':pageData}
    return res
    
@bp.route('/getAuth', methods=('GET', 'POST'))
def get_auth():
    res = {'info':{'state':'1', 'dongle_status':1, 'expire_hour':222, 'remark':'remark', 'create_date_str':'create_date_str', 'expire_date_str':'expire_date_str'}}
    return res
    
@bp.route('/getCheckNewData', methods=('GET', 'POST'))
def get_check_new_data():
    data = []
    res = {'info':{'audio_path':'path', 'alarm':'alaram', 'imageUrlArray':['a.jpg', 'b.jpg']}, 'data':data, 'code':0}
    return res
