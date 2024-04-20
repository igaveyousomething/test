import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db, query_db
from .utils.Utils import buildPageLabels

bp = Blueprint('open', __name__, url_prefix='/open')

@bp.route('/index', methods=('GET', 'POST'))
def index():
    data = []
#    for item in query_db('select * from av_algorithm_flow'):
#        data.append(item)
    g.data = data
    g.pageData = { 'page_num':1, 'count':len(data), 
                'pageLabels':buildPageLabels(1, 1)}
    return render_template('open/index.html')
    
@bp.route('/add', methods=('GET', 'POST'))
def add():
    stream = {'is_online':'super'}
    g.obj = {'app':'app', 'name':'name', 'wsMp4Url':'/static/images/user.png', 
                'wsMp4Url':'wsMp4Url', 'code':0, 'rtspUrl':'rtspUrl', 'hlsUrl':'hlsUrl',
                'nickname':'nickname', 'remark':'remark', 
                'author':'author', 'pull_stream_url':'pull_stream_url'}
    g.handle = "add"
    g.control_stream = "add"
    g.open = {}
    return render_template('open/add.html')
    
@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    stream = {'is_online':'super'}
    g.obj = {'app':'app', 'name':'name', 'wsMp4Url':'/static/images/user.png', 
                'wsMp4Url':'wsMp4Url', 'code':0, 'rtspUrl':'rtspUrl', 'hlsUrl':'hlsUrl',
                'nickname':'nickname', 'remark':'remark', 
                'author':'author', 'pull_stream_url':'pull_stream_url'}
    g.handle = 'edit'
    g.control_stream = 'edit'
    g.open = {}
    return render_template('open/add.html')
    
@bp.route('/view', methods=('GET', 'POST'))
def view():
    stream = {'is_online':'super'}
    g.obj = {'app':'app', 'name':'name', 'wsMp4Url':'/static/images/user.png', 
                'wsMp4Url':'wsMp4Url', 'code':0, 'rtspUrl':'rtspUrl', 'hlsUrl':'hlsUrl',
                'nickname':'nickname', 'remark':'remark', 
                'author':'author', 'pull_stream_url':'pull_stream_url'}
    g.handle = 'edit'
    g.control_stream = 'edit'
    g.open = {}
    return render_template('open/view.html')
    
@bp.route('/postDel', methods=('GET', 'POST'))
def post_del():
    res = {'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res
    
@bp.route('/getPatrol', methods=('GET', 'POST'))
def get_patrol():
    res = {'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res
    
