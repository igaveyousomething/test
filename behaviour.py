import functools
import time
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db, query_db, insert_db, delete_db, update_db
from .utils.Utils import buildPageLabels, gen_code

bp = Blueprint('behaviour', __name__, url_prefix='/behaviour')

@bp.route('/index', methods=('GET', 'POST'))
def index():
    data = []
    for item in query_db('select * from av_behaviour'):
        data.append(item)
    g.data = data
    g.pageData = { 'page_num':1, 'count':len(data), 
                'pageLabels':buildPageLabels(1, 1)}
    return render_template('behaviour/index.html')
    
@bp.route('/add', methods=('GET', 'POST'))
def add():
    g.handle = "add"
    # TODO:接入方式从哪里引入
    g.behaviour_ways = [{'code':'API', 'name':'API'},{'code':'SYSTEM', 'name':'SYSTEM'},{'code':'LIBRARY', 'name':'LIBRARY'}]
    new_code = gen_code('behaviour')
    g.behaviour = {'code':new_code}
    data = []
    if request.method == 'POST':
        name = request.form["name"]
        way_code = request.form["way_code"]
        way_value = request.form["way_value"]
        data = [new_code, name, way_code, way_value]
        cur_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
        insert_sql = "INSERT INTO av_behaviour(user_id, sort, code, name, way_code,way_value, create_time, last_update_time, state, from_source, extend_params, remark) VALUES(?,?,?,?,?,?,?,?,?,?,?,?);" 
        insert_db(insert_sql, args=(1, 0, new_code, name, way_code, way_value, cur_time, cur_time, 0,0,'',''))
        return redirect(url_for('behaviour.index'))
    return render_template('behaviour/add.html')
    
@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    g.behaviour_ways = [{'code':'API', 'name':'API'},{'code':'SYSTEM', 'name':'SYSTEM'},{'code':'LIBRARY', 'name':'LIBRARY'}]
    g.handle = 'edit'
    code1 = request.args.get("code")
    if request.method == 'POST':
        name = request.form["name"]
        way_value = request.form["way_value"]
        update_db('update av_behaviour set name=? , way_value=? where code=?',(name, way_value, code1))
        return redirect(url_for('behaviour.index'))
    else:
        result = query_db('select * from av_behaviour where code = ?', [code1], one=True)
        # TODO: 提示
        if result is None:
            print('No result')
            g.behaviour = {}
        else:
            g.behaviour = result

    return render_template('behaviour/add.html')
    
@bp.route('/postDel', methods=('GET', 'POST'))
def post_del():
    code1 = request.form['code']
    delete_db("delete from av_behaviour where code = ?", [code1])
    res = {'code':1000, 'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res
    
