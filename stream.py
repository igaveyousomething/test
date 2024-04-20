import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from .utils.ZLMediaKit import ZLMediaKit

bp = Blueprint('stream', __name__, url_prefix='/stream')

global res
res = {}

@bp.route('/index', methods=('GET', 'POST'))
def index():
    stream = {'is_online':'super'}
    settings = {'name':'name', 'welcome':'welcome', 'logo_url':'/static/images/user.png', 
                'bottom_name':'bottom_name', 'is_show_author':1, 'author_link':'link', 
                'author':'author'}
    g.settings = settings
    return render_template('stream/index.html')
    
@bp.route('/add', methods=('GET', 'POST'))
def add():
    stream = {'is_online':'super'}
    g.obj = {'app':'app', 'name':'name', 'wsMp4Url':'/static/images/user.png', 
                'wsMp4Url':'wsMp4Url', 'code':0, 'rtspUrl':'rtspUrl', 'hlsUrl':'hlsUrl',
                'nickname':'nickname', 'remark':'remark', 
                'author':'author', 'pull_stream_url':'pull_stream_url'}
    g.handle = 'add'
    return render_template('stream/add.html')
    
@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    stream = {'is_online':'super'}
    g.obj = {'app':'app', 'name':'name', 'wsMp4Url':'/static/images/user.png', 
                'wsMp4Url':'wsMp4Url', 'code':0, 'rtspUrl':'rtspUrl', 'hlsUrl':'hlsUrl',
                'nickname':'nickname', 'remark':'remark', 
                'author':'author', 'pull_stream_url':'pull_stream_url'}
    g.handle = 'edit'
    return render_template('stream/add.html')
    
@bp.route('/multiplayer', methods=('GET', 'POST'))
def multiplayer():
    stream = {'is_online':'super'}
    g.obj = {'app':'app', 'name':'name', 'wsMp4Url':'/static/images/user.png', 
                'wsMp4Url':'wsMp4Url', 'code':0, 'rtspUrl':'rtspUrl', 'hlsUrl':'hlsUrl',
                'nickname':'nickname', 'remark':'remark', 
                'author':'author', 'pull_stream_url':'pull_stream_url'}
    return render_template('stream/multiplayer.html')
    

@bp.route('/player', methods=('GET', 'POST'))
def player():
    app_n = request.args.get("app")
    name = request.args.get("name")
    
    g.stream = {'is_online': 1, 'app': app_n, 'name': name, 'video_codec_name': 'h264',\
     'video_width': 1920, 'video_height': 1080, 'wsHost': 'ws://127.0.0.1:9002',\
      'wsMp4Url': 'ws://127.0.0.1:9002/{0}/{1}.{0}.mp4'.format(app_n, name), 'wsFlvUrl': 'ws://127.0.0.1:9002/{0}/{1}.{0}.flv'.format(app_n, name),\
       'httpMp4Url': 'http://127.0.0.1:9002/{0}/{1}.{0}.mp4'.format(app_n, name), 'httpFlvUrl': 'http://127.0.0.1:9002/{0}/{1}.{0}.flv'.format(app_n, name),\
        'rtspUrl': 'rtsp://127.0.0.1:9554/{0}/{1}'.format(app_n, name)}
    g.is_exist_stream = 1
    print(res)
    return render_template('stream/player2.html')
    
@bp.route('/online', methods=('GET', 'POST'))
def online():
    stream = {'is_online':'super'}
    settings = {'name':'name', 'welcome':'welcome', 'logo_url':'/static/images/user.png', 
                'bottom_name':'bottom_name', 'is_show_author':1, 'author_link':'link', 
                'author':'author'}
#    g.res = []
    config = {'host': '127.0.0.1', 'adminPort': 9001, 'mediaHttpPort': 9002, 'analyzerPort': 9003,
              'mediaRtspPort': 9554, 'videoAnalyzerPort': 9555, 'mediaSecret': 'aqxY9ps21fyhyKNRyYpGvJCTp1JBeGOM',
              'trtexec': 'Analyzer\\trtexec.exe', 'fontPath': 'Analyzer\\fonts\\tsimhei.ttf',
              'uploadDir': 'Admin\\static\\upload', 'mediaRootDir': 'MediaServer/www', 'autoAddAllForward': True,
              'autoManagePatrolForward': False, 'cacheModelMaxDuration': 120000, 'enableHardwareDecode': False,
              'hardwareDecodeMaxCount': 1, 'hardwareDecoder': 'nvidia', 'enableHardwareEncode': False,
              'hardwareEncodeMaxCount': 0, 'hardwareEncoder': 'nvidia'}
    
    return render_template('stream/online.html')

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
    
@bp.route('/getOnline', methods=('GET', 'POST'))
def get_online():
    ConfigObj = {\
    "mediaApiHost"  : "http://127.0.0.1:9002",\
    "mediaHttpHost" : "http://127.0.0.1:9001",\
    "mediaRtmpHost" : "rtmp://127.0.0.1:1935",\
    "mediaRtspHost" : "rtsp://127.0.0.1:9554",\
    # "analyzerApiHost" : "http://127.0.0.1:9002"\
    "analyzerApiHost" : "http://127.0.0.1:9003"\
}
    zlm = ZLMediaKit(ConfigObj)
    data = zlm.getMediaList()
    if len(data) > 0:
        res = {'code':1000,'data':data}
    else:
        res = {'code':500, 'data':[]}
    return res
    
@bp.route('/getAllUpdateForwardState', methods=('GET', 'POST'))
def get_all_update_forward_state():
    res = {'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res
    
@bp.route('/postDel', methods=('GET', 'POST'))
def post_del():
    res = {'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res

@bp.route('/postImportFile', methods=('GET', 'POST'))
def post_import_file():
    res = {'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
    return res
    
@bp.route('/postHandleForward', methods=('GET', 'POST'))
def post_handle_forward():
    res = {'data':[{'source_type':1, 'clients':1, 'produce_speed':1, 'video':'video', 'audio':'audio'}]}
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