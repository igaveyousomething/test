import functools
import time
import threading
import subprocess

import cv2
import ffmpeg

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db, query_db, insert_db, delete_db, update_db
from .utils.Utils import buildPageLabels, gen_code
from .utils.ZLMediaKit import ZLMediaKit
from .resolve_yolo import Worker

bp = Blueprint('control', __name__, url_prefix='/control')
w = Worker()
new_code = gen_code('control')

@bp.route('/index', methods=('GET', 'POST'))
def index():
    
    stream = {'is_online':'super'}
    g.control = { 'page_num':1, 'count':1, 
                'pageLabels':[{'cur':1, 'name':'name'}, {'cur':2, 'name':'name2'}]}
                
    data = []
    for item in query_db("SELECT id, code, name, algorithm_type as algorithm_type_name, way_code||'/'||framework||'/'||inference as way , last_update_time FROM av_algorithm"):
        data.append(item)
    g.data = data
    g.pageData = { 'page_num':1, 'count':len(data), 'page_size':1,
                'pageLabels':buildPageLabels(1, 1)}
    return render_template('control/index.html')
    
@bp.route('/add', methods=('GET', 'POST'))
def add():
    g.handle = "add"
    
    g.control_stream = "add"
    g.control = {'code':new_code, 'push_stream':0, 'min_interval':180, 'overlap_thresh':0.5, 'alarm_image_count':5,\
                'alarm_monitor_duration':120, 'alarm_draw_type':0}
    # 视频流
    ConfigObj = {\
    "mediaApiHost"  : "http://127.0.0.1:9002",\
    "mediaHttpHost" : "http://127.0.0.1:9001",\
    "mediaRtmpHost" : "rtmp://127.0.0.1:1935",\
    "mediaRtspHost" : "rtsp://127.0.0.1:9554",\
    # "analyzerApiHost" : "http://127.0.0.1:9002"\
    "analyzerApiHost" : "http://127.0.0.1:9003"\
    }
    zlm = ZLMediaKit(ConfigObj)
    stream_data = zlm.getMediaList()
    print(stream_data)
    g.streams = stream_data
    # 算法
    data = []
    for item in query_db("SELECT * FROM av_algorithm_flow"):
        data.append(dict(item))
    g.flows = data
    # 音频流
    data = []
    for item in query_db("SELECT * FROM av_audio"):
        data.append(dict(item))
    g.audios = data
    print(data)
    # 报警接口
    data = []
    for item in query_db("SELECT * FROM av_alarm_interface"):
        data.append(item)
    g.alarmInterfaces = data

    return render_template('control/add.html')
    
@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    stream = {'is_online':'super'}
    g.obj = {'app':'app', 'name':'name', 'wsMp4Url':'/static/images/user.png', 
                'wsMp4Url':'wsMp4Url', 'code':0, 'rtspUrl':'rtspUrl', 'hlsUrl':'hlsUrl',
                'nickname':'nickname', 'remark':'remark', 
                'author':'author', 'pull_stream_url':'pull_stream_url'}
    g.handle = 'edit'
    g.control_stream = 'edit'
    g.control = {}
    return render_template('control/add.html')
    
@bp.route('/postDel', methods=('GET', 'POST'))
def post_del():
    code1 = request.form['controlCode']
    print(code1)
    delete_db("delete from av_control where code = ?", [code1])
    res = {'code':1000, 'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res
    
@bp.route('/postCopy', methods=('GET', 'POST'))
def post_copy():
    res = {'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res   
     
@bp.route('/postAddControl', methods=('GET', 'POST'))
def post_add_control():
    control_code = request.form['controlCode']
    t1 = threading.Thread(target=w.main_worker, args=(control_code,'',0, 'yolov8n'))
    t1.start()
    update_db("update av_control set state=1 where code =?", [control_code])
    res = {'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}], 'code':1000}
    return res      
    
@bp.route('/postAdd', methods=('GET', 'POST'))
def post_add():
    print(request.form.keys())
    cur_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
    stream_app = request.form["streamApp"]
    stream_name = request.form["streamName"]
    stream_video = request.form["streamVideo"]
    stream_audio = request.form["streamAudio"]
    
    push_stream = request.form["pushStream"]
    
    push_stream_app = 'analyzer'
    push_stream_name = new_code
    
    flow_code = request.form["flowCode"]
    min_interval = request.form["minInterval"]
    overlap_thresh = request.form["overlapThresh"]
    polygon = request.form["polygon"]
    polygon_type = request.form["polygon_type"]
    audio_code = request.form["audioCode"]
    
    alarm_interface_code = request.form["alarmInterfaceCode"]
    alarm_image_count = request.form["alarmImageCount"]
    alarm_monitor_duration = request.form["alarmMonitorDuration"]
    alarm_draw_type = request.form["alarmDrawType"]
    osd_params = request.form["osd_params"]
    extend_params = request.form["extend_params"]
    remark = request.form["remark"]     
    
    insert_sql = "INSERT INTO av_control(user_id, sort, code, stream_app, stream_name, stream_video, stream_audio, push_stream, push_stream_app, push_stream_name, flow_code, min_interval, overlap_thresh, polygon, polygon_type, audio_code, alarm_interface_code, alarm_image_count, alarm_monitor_duration, alarm_draw_type, osd_params, extend_params, remark, create_time, last_update_time, add_type, state) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);" 
    insert_db(insert_sql, args=(1, 0, new_code, stream_app, stream_name, stream_video, stream_audio, push_stream, push_stream_app, push_stream_name, flow_code, min_interval, overlap_thresh, polygon, polygon_type, audio_code, alarm_interface_code, alarm_image_count, alarm_monitor_duration, alarm_draw_type, osd_params, extend_params, remark, cur_time, cur_time, 0,0))
    res = {'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}], 'code':1000}
    return res  
      
@bp.route('/postCancelControl', methods=('GET', 'POST'))
def post_cancel_control():
    control_code = request.form['controlCode']
    w.stop_stream()
    update_db("update av_control set state=0 where code =?", [control_code])
    res = {'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}], 'code':1000}
    return res
    
@bp.route('/getIndex', methods=('GET', 'POST'))
def get_index():
    ConfigObj = {
        "mediaApiHost"  : "http://127.0.0.1:9002",
        "mediaHttpHost" : "http://127.0.0.1:9001",
        "mediaRtmpHost" : "rtmp://127.0.0.1:1935",
        "mediaRtspHost" : "rtsp://127.0.0.1:9554",
        "analyzerApiHost" : "http://127.0.0.1:9003"
        }
    zlm = ZLMediaKit(ConfigObj)
    stream_data = zlm.getMediaList()
    
    data = []
    for item in query_db("SELECT av_control.*, av_control.stream_name as stream_nickname, av_control.state as cur_state,av_algorithm_flow.name as flow_nickname  FROM av_control left join av_algorithm_flow where av_control.flow_code=av_algorithm_flow.code"):
        data.append(dict(item))
    res = {'data':data, 'code':1000, 'info':{'online_stream_len':len(stream_data),'online_control_len':1}, 'pageData':{'page_size':1, 'count':len(data), 'page_size':1,'page_num':1,
                'pageLabels':buildPageLabels(1, 1)}}
    return res


