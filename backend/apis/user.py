# -*-coding:utf-8-*-
from flask import session
from .common import ApiAction, request_method_check, Argument, parse_arguments
from backend.models import User
from flask_login import current_user

import random


class UserApi(ApiAction):
    @request_method_check(['POST'])
    @parse_arguments(
        Argument('mobile', int, required=True),
        Argument('password1', str, required=True),
        Argument('password2', str, required=True),
        Argument('verify_code', int, required=True))
    def create_user(self, arguments):
        user_exist = User.find_one(mobile=arguments['mobile'])
        if user_exist:
            return self.is_fail('当前手机号码已被注册')
        if arguments['verify_code'] != session[str(arguments['mobile'])]:
            return self.is_fail('验证码不正确')
        user = User(arguments['mobile'], arguments['password1'])
        result = user.save()
        return self.is_done(result)

    @request_method_check(['GET'])
    @parse_arguments(Argument('mobile', int, required=True))
    def get_verify_code(self, arguments):
        # ToDO:待添加短信发送模块
        random_list = random.sample(range(10), 6)
        verify_code = ''.join(str(i) for i in random_list)
        session[str(arguments['mobile'])] = verify_code
        return self.is_done({'verify_code': verify_code})

    @request_method_check(['GET'])
    def get_current_user(self, arguments):
        return self.is_done(dict(current_user))
