import os

from flask import Flask, g, session

from . import db, auth, blog, stream, version, system, index, \
            alarm, alarmInterface, algorithmFlow, algorithm, behaviour, \
            control, controlPatrol, audio, open, user

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'Admin.sqlite3'),
    )
    
    
    
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(version.bp)
    app.register_blueprint(stream.bp)
    app.register_blueprint(system.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(alarm.bp)
    app.register_blueprint(alarmInterface.bp)
    app.register_blueprint(algorithm.bp)
    app.register_blueprint(algorithmFlow.bp)
    app.register_blueprint(behaviour.bp)
    app.register_blueprint(control.bp)
    app.register_blueprint(audio.bp)
    app.register_blueprint(open.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(controlPatrol.bp)
#    app.add_url_rule('/', endpoint='index')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/')
    def main_page():
        return render_template('app/web_index.html')

    return app
    
    
