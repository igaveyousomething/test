import functools
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db, query_db, insert_db, delete_db, update_db
from .utils.Utils import buildPageLabels, gen_code

bp = Blueprint('audio', __name__, url_prefix='/audio')

@bp.route('/index', methods=('GET', 'POST'))
def index():
    stream = {'is_online':'super'}
    g.audio = { 'page_num':1, 'count':1, 
                'pageLabels':[{'cur':1, 'name':'name'}, {'cur':2, 'name':'name2'}]}
    g.pageData = { 'page_num':1, 'count':1, 
                'pageLabels':[{'cur':1, 'name':'name'}, {'cur':2, 'name':'name2'}]}
                
    data = []
    for item in query_db("SELECT * FROM av_audio"):
        data.append(item)
    g.data = data
    g.pageData = { 'page_num':1, 'count':len(data), 
                'pageLabels':buildPageLabels(1, 1)}
    return render_template('audio/index.html')
    
@bp.route('/add', methods=('GET', 'POST'))
def add():
    g.handle = "add"
    new_code = gen_code('audio')
    g.audio = {'code':new_code}
    
    if request.method == 'POST':
        cur_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
        name = request.form["name"]
        extend_params = request.form["extend_params"]
        remark = request.form["remark"]
        path = 'path'   #TODO:
        insert_sql = "INSERT INTO av_audio(user_id, sort, code, name, extend_params, remark, create_time, last_update_time, state, from_source ,audio_path) VALUES(?,?,?,?,?,?,?,?,?,?,?);" 
        insert_db(insert_sql, args=(1, 0, new_code, name, extend_params, remark,cur_time, cur_time, 0,0, path))
        return redirect(url_for('audio.index'))

    return render_template('audio/add.html')
    
@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    g.handle = 'edit'
    g.audio = {}
    cur_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
    code1 = request.args.get("code")
    result = query_db('select * from av_audio where code = ?',
                [code1], one=True)
    if result is None:
        print('No result')
    else:
        g.audio = result
    g.absolute_audio_path = 'flaskr/static/upload/audio'+result['audio_path']     # 临时的，需要绝对路径
    if request.method == 'POST':
        name = request.form['name']
        extend_params = request.form['extend_params']
        remark = request.form['remark']
        update_db('update av_audio set name=?, extend_params=?, remark = ?, last_update_time=? where code=?',(name, extend_params, remark, cur_time, code1))
        return redirect(url_for('audio.index'))
    return render_template('audio/add.html')
    
@bp.route('/view', methods=('GET', 'POST'))
def view():
    stream = {'is_online':'super'}
    g.obj = {'app':'app', 'name':'name', 'wsMp4Url':'/static/images/user.png', 
                'wsMp4Url':'wsMp4Url', 'code':0, 'rtspUrl':'rtspUrl', 'hlsUrl':'hlsUrl',
                'nickname':'nickname', 'remark':'remark', 
                'author':'author', 'pull_stream_url':'pull_stream_url'}
    g.handle = 'edit'
    g.control_stream = 'edit'
    g.audio = {}
    return render_template('audio/view.html')
    
@bp.route('/postDel', methods=('GET', 'POST'))
def post_del():
    code1 = request.form['code']
    delete_db("delete from av_audio where code = ?", [code1])
    res = {'code':1000, 'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res
    
@bp.route('/getPatrol', methods=('GET', 'POST'))
def get_patrol():
    res = {'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res
    
