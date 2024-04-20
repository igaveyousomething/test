import functools
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db, query_db, insert_db, delete_db, update_db
from .utils.Utils import buildPageLabels, gen_code

bp = Blueprint('alarmInterface', __name__, url_prefix='/alarmInterface')

@bp.route('/index', methods=('GET', 'POST'))
def index():
    data = []
    for item in query_db("SELECT * FROM av_alarm_interface"):
        data.append(item)
    g.data = data
    g.pageData = { 'page_num':1, 'count':len(data), 'page_size':1,
                'pageLabels':buildPageLabels(1, 1)}    
    return render_template('alarmInterface/index.html')
    
@bp.route('/add', methods=('GET', 'POST'))
def add():
    g.handle = 'add'
    new_code = gen_code('ai')
    g.obj = {'name':'', 'code': new_code, 'request_address':'', 'request_params':'', 'alarm_delay':0, 'request_server_type':0,
                'is_save_local':1, 'request_content_extend_params':'version=4.40,flag=pub20240113', 'remark':''}
    
    if request.method == 'POST':
        cur_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
        name = request.form["name"]
        is_save_local = request.form['is_save_local']
        request_address = request.form['request_address']
        request_params = request.form['request_params']
        request_server_type = request.form['request_server_type']
        request_content_extend_params = request.form['request_content_extend_params']
        remark = request.form["remark"]
        alarm_delay = request.form['alarm_delay']
        insert_sql = "INSERT INTO av_alarm_interface(user_id, sort, code, name, is_save_local, request_address, request_params, request_server_type, request_content_extend_params, remark, alarm_delay, create_time, last_update_time, state, from_source) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);" 
        insert_db(insert_sql, args=(1, 0, new_code, name, is_save_local, request_address, request_params, request_server_type, request_content_extend_params, remark, alarm_delay, cur_time,cur_time,1,0))
        return redirect(url_for('alarmInterface.index'))
    
    return render_template('alarmInterface/add.html')
    
@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    cur_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
    g.handle = 'edit'
    # main info
    code1 = request.args.get("code")
    result = query_db('select * from av_alarm_interface where code = ?',
                [code1], one=True)
    g.obj = result
    # 提交编辑
    if request.method == 'POST':
        name = request.form['name']
        is_save_local = request.form['is_save_local']
        request_address = request.form['request_address']
        request_params = request.form['request_params']
        request_server_type = request.form['request_server_type']
        request_content_extend_params = request.form['request_content_extend_params']
        remark = request.form['remark']
        alarm_delay = request.form['alarm_delay']
        update_db('update av_alarm_interface set name=?, is_save_local=?, request_address=?, request_params=?, request_server_type=?, request_content_extend_params=?, remark = ?, alarm_delay=?, last_update_time=? where code=?', \
                    (name, is_save_local, request_address, request_params, request_server_type, request_content_extend_params, remark, alarm_delay, cur_time, code1))
        return redirect(url_for('alarmInterface.index'))
    return render_template('alarmInterface/add.html')
    
    
@bp.route('/postTest', methods=('GET', 'POST'))
def post_test():
    res = {'osInfo':[{'os_cpu_used_rate':20, 'os_virtual_mem_used_rate':1, 'os_disk_used_rate':22,
            'os_cpu_used_rate_str':22, 'os_virtual_mem_used_rate_str':23, 
            'os_disk_used_rate_str':23, 'os_run_date_str':23, }]}
    return res   
     
@bp.route('/postDel', methods=('GET', 'POST'))
def post_del():
    code1 = request.form['code']
    print(code1)
    delete_db("delete from av_alarm_interface where code = ?", [code1])
    res = {'code':1000, 'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res
