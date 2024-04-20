import functools
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db, query_db, insert_db, delete_db, update_db
from .utils.Utils import buildPageLabels, gen_code

bp = Blueprint('algorithm', __name__, url_prefix='/algorithm')

@bp.route('/index', methods=('GET', 'POST'))
def index():
    data = []
    for item in query_db("SELECT id, code, name, algorithm_type as algorithm_type_name, way_code||'/'||framework||'/'||inference as way , last_update_time FROM av_algorithm"):
        data.append(item)
    g.data = data
    g.pageData = { 'page_num':1, 'count':len(data), 
                'pageLabels':buildPageLabels(1, 1)}
    return render_template('algorithm/index.html')
    
@bp.route('/add', methods=('GET', 'POST'))
def add():
    g.handle = "add"
    # TODO:数据从哪里引入
    g.algorithm_ways = [{'code':'API', 'name':'API'},{'code':'MODEL', 'name':'MODEL'}]
    g.algorithm_types = [{'code':'Detect', 'name':'检测算法'},{'code':'Classify', 'name':'分类算法'},{'code':'Track', 'name':'追踪算法'}]
    new_code = gen_code('algorithm')
    g.algorithm = {'code':new_code, 'inference_device':'GPU', \
                    'extend_params': 'width=640,height=640,nms_threshold=0.5,score_threshold=0.5,fp=16', \
                    'model_convert_params': '--fp16'}
    
    if request.method == 'POST':
        cur_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
        name = request.form["name"]
        way_code = request.form["way_code"]
        algorithm_type = request.form["algorithm_type"]
        print(request.form.keys())
        if way_code == 'MODEL':
            way_value = ''
            framework = request.form["framework"]
            inference = request.form["inference"]
            inference_device = request.form["inference_device"]
            model_name = request.form["model_name"]
            model_name_dir = request.form["model_name_dir"]
            model_class_names = request.form["model_class_names"]
            model_convert_params = request.form["model_convert_params"]
            extend_params = request.form["extend_params"]
            remark = ''
        else:
            way_value = request.form["way_value"]
            framework = ''
            inference = ''
            inference_device = ''
            model_name = ''
            model_name_dir = ''
            model_class_names = ''
            model_convert_params = ''
            extend_params = ''
            remark = ''
        insert_sql = "INSERT INTO av_algorithm(user_id, sort, code, name, control_max_count, way_code,way_value, algorithm_type, framework, inference, inference_device, model_name, model_name_dir, model_class_names, model_convert_params, extend_params, remark, create_time, last_update_time, state, from_source ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);" 
        insert_db(insert_sql, args=(1, 0, new_code, name, 0, way_code, way_value, algorithm_type, framework,inference, inference_device, model_name, model_name_dir, model_class_names, model_convert_params, extend_params, remark,cur_time, cur_time, 0,0))
#        return redirect(url_for('algorithm.index'))
    return render_template('algorithm/add.html')
    
@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    stream = {'is_online':'super'}
    g.obj = {'app':'app', 'name':'name', 'wsMp4Url':'/static/images/user.png', 
                'wsMp4Url':'wsMp4Url', 'code':0, 'rtspUrl':'rtspUrl', 'hlsUrl':'hlsUrl',
                'nickname':'nickname', 'remark':'remark', 
                'author':'author', 'pull_stream_url':'pull_stream_url'}
    g.handle = 'edit'
    g.algorithm = {}
    return render_template('algorithm/add.html')
       
@bp.route('/postDel', methods=('GET', 'POST'))
def post_del():
    code1 = request.form['code']
    delete_db("delete from av_algorithm where code = ?", [code1])
    res = {'code':1000, 'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res
       
      
@bp.route('/postAlgorithmTypeAttrs', methods=('GET', 'POST'))
def post_algorithm_type_attrs():
    algorithm_type_code = request.form['algorithm_type_code']
    if algorithm_type_code == 'Detect':
        res = {'info':{'frameworks':['YOLO8','YOLO8-POSE','YOLO5'],'inferences':['OpenVINO','TensorRT']}, 'code':1000}
    elif algorithm_type_code == 'Classify':
        res = {'info':{'frameworks':['YOLO8','ResNet50'],'inferences':['OpenVINO','TensorRT']}, 'code':1000}
    elif algorithm_type_code == 'Track':
        res = {'info':{'frameworks':['DeepSort'],'inferences':['TensorRT']}, 'code':1000}
    return res


