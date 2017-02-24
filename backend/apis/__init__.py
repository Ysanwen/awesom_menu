# -*-coding:utf-8-*-

from flask_restful import Api
from flask import Blueprint
from backend import app

from .test import *
from .user import *
from .uploadfile import *
from .menu import *

api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(api_bp)

api.add_resource(TestApi, "/test", "/test/<string:action>")
api.add_resource(UserApi, "/user", "/user/<string:action>")
api.add_resource(UploadFileApi, "/upload", "/upload/<string:action>")
api.add_resource(MenuApi, "/menu", "/menu/<string:action>")

app.register_blueprint(api_bp)
