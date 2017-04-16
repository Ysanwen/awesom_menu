# -*-coding:utf-8-*-

from .common import BaseModel
import sqlalchemy
from uuid import uuid1
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from backend import login_manager
import pytz
import pickle


@BaseModel.register_table()
class User(BaseModel):
    # uid_filed = {'uid': 0}
    __column_fileds__ = {
        # 'uid': sqlalchemy.Integer,
        'id': sqlalchemy.String,
        'username': sqlalchemy.String(50),
        'password': sqlalchemy.String,
        'mobile': sqlalchemy.BigInteger,
        'create_time': sqlalchemy.DateTime,
        'ad': sqlalchemy.String,
        'url_list': sqlalchemy.String,
        'isActive': sqlalchemy.Boolean
    }

    def __init__(self, mobile, password, id=str(uuid1()), username=''):
        # self.uid = self.uid_filed['uid'] + 1
        self.id = id
        self.username = username
        self.password = generate_password_hash(password)
        self.mobile = mobile
        self.create_time = datetime.now(pytz.timezone('Asia/Shanghai'))
        self.ad = ''
        self.url_list = ''
        self.isActive = True

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

    # 用户登录处理相关
    @property
    def is_authenticated(self):
        """
        通过验证的用户返回true,只有通过验证的用户满足login_required
        """
        return True

    @property
    def is_active(self):
        """
        活动用户且通过验证，账户也已激活，未被停用
        """
        return True

    @property
    def is_anonymous(self):
        """
        匿名用户则返回true
        """
        return False

    def get_id(self):
        """
        返回一个能唯一识别用户的id,unicode类型
        """
        return str(self.id)


@login_manager.user_loader
def load_user(uid):
    user = User.find_by_id(uid)
    if user:
        if('url_list' in user and user['url_list']):
            user['url_list'] = pickle.loads(user['url_list'])
        else:
            user['url_list'] = []
        if('password' in user):
            del user['password']
        new_instance = User('default', 'default')
        for k in user.keys():
            setattr(new_instance, k, user[k])
            new_instance[k] = user[k]
        return new_instance
    else:
        return None
