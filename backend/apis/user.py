# -*-coding:utf-8-*-
import os
import uuid
import pickle
import random
import json
from flask import session, request
from .common import ApiAction, request_method_check, Argument, parse_arguments
from backend.models import User
from flask_login import current_user
from werkzeug.security import generate_password_hash


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
        if str(arguments['verify_code']) != str(session[str(arguments['mobile'])]):
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

    @request_method_check(['GET'])
    @parse_arguments(Argument('mobile', int, required=True))
    def verify_code_for_reset(self, arguments):
        # ToDO:待添加短信发送模块
        has_num = User.find_one(mobile=arguments['mobile'])
        if not has_num:
            return self.is_fail('手机号码不正确')
        random_list = random.sample(range(10), 6)
        verify_code = ''.join(str(i) for i in random_list)
        session[str(arguments['mobile'])] = verify_code
        return self.is_done({'verify_code': verify_code})

    @request_method_check(['POST'])
    @parse_arguments(
        Argument('mobile', int, required=True),
        Argument('password', str, required=True),
        Argument('verify_code', int, required=True))
    def reset_password(self, arguments):
        user_exist = User.find_one(mobile=arguments['mobile'])
        if not user_exist:
            return self.is_fail('手机号码不正确')
        if str(arguments['verify_code']) != str(session[str(arguments['mobile'])]):
            return self.is_fail('验证码不正确')
        result = User.update({
            'mobile': arguments['mobile'],
            'password': generate_password_hash(arguments['password'])}, ['mobile'])
        return self.is_done('success') if result else self.is_fail('重置失败')

    @request_method_check(['POST'])
    @parse_arguments(
        Argument('ad', str, required=True),
        Argument('username', str, required=True),
        Argument('url_list', str, required=True))
    def create_info(self, arguments):
        url_list = arguments['url_list']
        # reload the url_list from str to list
        arguments['url_list'] = json.loads(url_list)

        file_dict = request.files.to_dict()
        if file_dict:
            # 保存文件后，更新new_url_list
            for k, v in file_dict.items():
                if v.mimetype.split('/')[0] != 'image':
                    return self.is_fail('upload file type is not image')
            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/upload')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            upload_url_list = []
            for key, file in file_dict.items():
                suffix = file.filename.split('.')[-1]
                filename = str(uuid.uuid1()) + '.' + suffix
                file.save(os.path.join(output_dir, filename))
                upload_url_list.append(filename)
            arguments['url_list'].extend(upload_url_list)
        arguments['url_list'] = pickle.dumps(arguments['url_list'])
        arguments['id'] = current_user['id']
        result = User.update(arguments, ['id'])
        return self.is_done('success') if result else self.is_fail('添加信息失败')

    @request_method_check(['GET'])
    @parse_arguments(Argument('uid', str, required=True))
    def get_restautant_info(self, arguments):
        data = {}
        user_info = User.find_one(id=arguments['uid'])
        if user_info:
            data['name'] = user_info['username']
            data['ad'] = user_info['ad']
            if('url_list' in user_info and user_info['url_list']):
                data['url_list'] = pickle.loads(user_info['url_list'])
            else:
                data['url_list'] = []
        return self.is_done(data)
