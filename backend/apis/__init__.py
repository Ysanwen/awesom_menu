# -*-coding:utf-8-*-

from flask_restful import Api
from flask import Blueprint
from backend import app

from .test import *
from .user import *
from .uploadfile import *
from .menu import *
from .qrcode_menu import *
from .order import *

api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(api_bp)

api.add_resource(TestApi, "/test", "/test/<string:action>")
api.add_resource(UserApi, "/user", "/user/<string:action>")
api.add_resource(UploadFileApi, "/upload", "/upload/<string:action>")
api.add_resource(MenuApi, "/menu", "/menu/<string:action>")
api.add_resource(CategoryApi, "category", "/category/<string:action>")
api.add_resource(QrcodeMenuApi, "/qrcode", "/qrcode/<string:action>")
api.add_resource(OrderApi, "/order", "/order/<string:action>")

app.register_blueprint(api_bp)
