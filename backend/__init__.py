# -*- coding:utf -8-*-

import importlib
from flask import Flask
from flask_script import Manager, Server as _Server
from flask_socketio import SocketIO
from .dataset import Dataset
from flask_login import LoginManager

app = Flask(__name__)


# 更改jinja的定界符，将模板内的{{ VALUE }}改成{{% VALUE %}}模式
new_jinja_con = app.jinja_options.copy()
new_jinja_con.update(dict(variable_start_string='{{%', variable_end_string='%}}'))
app.jinja_options = new_jinja_con

db = Dataset(app)
socketio = SocketIO(app)
manager = Manager(app)

login_manager = LoginManager()
login_manager.init_app(app)

# add socketio for script


class Server(_Server):
    def __call__(self, app, host, port, use_debugger, use_reloader, *args, **kwargs):
        # override the default runserver command to start a Socket.IO server
        if use_debugger is None:
            use_debugger = app.debug
            if use_debugger is None:
                use_debugger = True
        if use_reloader is None:
            use_reloader = app.debug
        socketio.run(app,
                     host=host,
                     port=port,
                     debug=use_debugger,
                     use_reloader=use_reloader,
                     **self.server_options)


manager.add_command("runserver", Server())


def create_app(env='development'):
    if env == 'production':
        app.config.from_object('backend.configs.%s' % env)
    else:
        app.config.from_object('backend.configs.development')
    if app.config.get("STATIC_FOLDER"):

        app.static_folder = app.config.get("STATIC_FOLDER")

    for module_name in ['backend.models', 'backend.views', 'backend.apis', 'backend.socketios']:
        importlib.import_module(module_name)

    return app
