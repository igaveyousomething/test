import functools
import sqlite3
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db, query_db, insert_db, delete_db, update_db
from .utils.Utils import buildPageLabels, gen_code

bp = Blueprint('algorithmFlow', __name__, url_prefix='/algorithmFlow')


@bp.route('/index', methods=('GET', 'POST'))
def index():  
    data = []
    for item in query_db('select id, code, name, max_concurrency, last_update_time, mode as mode_remark from av_algorithm_flow'):
        data.append(item)
    g.data = data
    g.pageData = { 'page_num':1, 'count':len(data), 
                'pageLabels':buildPageLabels(1, 1)}
    # TODO: 没分页
    return render_template('algorithmFlow/index.html')
    
@bp.route('/add', methods=('GET', 'POST'))
def add():
    stream = {'is_online':'super'}
    new_code = gen_code('flow')
    g.flow = {'code':new_code, 'max_concurrency':1, 'concurrency_unit_length':1}          
    g.modes = [{'name':'检测', 'id':1, 'code':'DETECT', 'state':1},{'name':'追踪', 'id':2, 'code':'TRACK', 'state':0}]
    data = []
    for item in query_db("select code, name,way_code from av_behaviour"):
        data.append(item)
    g.behaviours = data
    data = []
    for item in query_db("select * from av_algorithm"):
        data.append(item)
    g.algorithm_detect_data = data
    g.handle = 'add'
    if request.method == 'POST':
        cur_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
        name = request.form["name"]
        mode = request.form["mode"]
        algorithm_detect_code = request.form["algorithm_detect_code"]
        algorithm_classify_code = ''
        detect_class_names = request.form["detect_class_names"]
        algorithm_track_code = request.form["algorithm_track_code"]
        behaviour_code = request.form["behaviour_code"]
        classify_class_names = ''
        max_concurrency = request.form["max_concurrency"]
        concurrency_unit_length = request.form["concurrency_unit_length"]
        extend_params = request.form["extend_params"]
        remark = request.form["remark"]
        create_time = cur_time
        last_update_time = cur_time
        add_type = 0
        state = 0
        from_source = 0
        
        insert_sql = "INSERT INTO av_algorithm_flow(user_id, sort, code, name, mode, algorithm_detect_code, algorithm_classify_code, algorithm_track_code, detect_class_names, classify_class_names, behaviour_code, max_concurrency, concurrency_unit_length, extend_params, remark, create_time, last_update_time, add_type, state, from_source) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);" 
        insert_db(insert_sql, args=(1, 0, new_code, name, mode, algorithm_detect_code, algorithm_classify_code, algorithm_track_code, detect_class_names, classify_class_names, behaviour_code, max_concurrency, concurrency_unit_length, extend_params, remark, create_time, last_update_time, add_type, state, from_source))
        return redirect(url_for('algorithmFlow.index'))
    return render_template('algorithmFlow/add.html')
    
@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    code = request.args.get("code")
    result = query_db('select * from av_algorithm_flow where code = ?',
                [code], one=True)
    if result is None:
        print('No result')
    else:
        g.flow = result
    
    g.modes = [{'name':'检测', 'id':1, 'code':'DETECT', 'state':1},{'name':'追踪', 'id':2, 'code':'TRACK', 'state':0}]
    data = []
    for item in query_db("select code, name,way_code from av_behaviour"):
        data.append(item)
    g.behaviours = data
    data = []
    for item in query_db("select * from av_algorithm"):
        data.append(item)
    g.algorithm_detect_data = data
    g.handle = 'edit'
    return render_template('algorithmFlow/add.html')
    
   
@bp.route('/postDel', methods=('GET', 'POST'))
def post_del():
    code1 = request.form['code']
    delete_db("delete from av_algorithm_flow where code = ?", [code1])
    res = {'code':1000, 'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    
    return res

