# -*-coding:utf-8-*-

from backend import app
from .views_blueprint import view_bp
from .main_view import *

app.register_blueprint(view_bp)
