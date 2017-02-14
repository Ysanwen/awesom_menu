# -*-coding:utf-8-*-

from flask_restful import Api
from flask import Blueprint
from backend import app

from .test import *

api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(api_bp)

api.add_resource(TestApi, "/test", "/test/<string:action>")


app.register_blueprint(api_bp)
