import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/index', methods=('GET', 'POST'))
def index():
    stream = {'is_online':'super'}
    g.user = { 'page_num':1, 'count':1, 
                'pageLabels':[{'cur':1, 'name':'name'}, {'cur':2, 'name':'name2'}]}
    g.pageData = { 'page_num':1, 'count':1, 
                'pageLabels':[{'cur':1, 'name':'name'}, {'cur':2, 'name':'name2'}]}
    return render_template('app/web_user_index.html')
    
@bp.route('/add', methods=('GET', 'POST'))
def add():
    stream = {'is_online':'super'}
    g.obj = {'app':'app', 'name':'name', 'wsMp4Url':'/static/images/user.png', 
                'wsMp4Url':'wsMp4Url', 'code':0, 'rtspUrl':'rtspUrl', 'hlsUrl':'hlsUrl',
                'nickname':'nickname', 'remark':'remark', 
                'author':'author', 'pull_stream_url':'pull_stream_url'}
    g.handle = "add"
    g.control_stream = "add"
    g.user = {}
    return render_template('user/add.html')
    
@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    stream = {'is_online':'super'}
    g.obj = {'app':'app', 'name':'name', 'wsMp4Url':'/static/images/user.png', 
                'wsMp4Url':'wsMp4Url', 'code':0, 'rtspUrl':'rtspUrl', 'hlsUrl':'hlsUrl',
                'nickname':'nickname', 'remark':'remark', 
                'author':'author', 'pull_stream_url':'pull_stream_url'}
    g.handle = 'edit'
    g.control_stream = 'edit'
    g.user = {}
    return render_template('user/add.html')
    
@bp.route('/view', methods=('GET', 'POST'))
def view():
    stream = {'is_online':'super'}
    g.obj = {'app':'app', 'name':'name', 'wsMp4Url':'/static/images/user.png', 
                'wsMp4Url':'wsMp4Url', 'code':0, 'rtspUrl':'rtspUrl', 'hlsUrl':'hlsUrl',
                'nickname':'nickname', 'remark':'remark', 
                'author':'author', 'pull_stream_url':'pull_stream_url'}
    g.handle = 'edit'
    g.control_stream = 'edit'
    g.user = {}
    return render_template('user/view.html')
    
@bp.route('/postDel', methods=('GET', 'POST'))
def post_del():
    res = {'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res
    
@bp.route('/getPatrol', methods=('GET', 'POST'))
def get_patrol():
    res = {'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res
    
