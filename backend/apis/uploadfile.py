# -*-coding:utf-8-*-
from .common import ApiAction, request_method_check, Argument, parse_arguments
from flask_login import current_user
from flask import request
import os
import uuid
import pickle
from backend.models import Menu, Category


class UploadFileApi(ApiAction):
    """
    upload file and store local
    should change to store online
    """
    @request_method_check(['POST'])
    @parse_arguments(
        Argument('name', str, required=True),
        Argument('unit', str, required=True),
        Argument('type', str, required=True),
        Argument('price', float, required=True),
        Argument('quantity', int, required=True),
        Argument('status', int, required=True))
    def upload_file(self, arguments):
        file_dict = request.files.to_dict()
        if not file_dict:
            return self.is_fail('no image file')
        for k, v in file_dict.items():
            if v.mimetype.split('/')[0] != 'image':
                return self.is_fail('upload file type is not image')
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/upload')
        url_list = []
        for key, file in file_dict.items():
            suffix = file.filename.split('.')[-1]
            filename = str(uuid.uuid1()) + '.' + suffix
            file.save(os.path.join(output_dir, filename))
            url_list.append(filename)

        uid = current_user['id']
        arguments.update({'uid': uid, 'url_address': pickle.dumps(url_list)})
        new_menu = Menu(**arguments)
        result = new_menu.save()

        # check whether there is a new type
        menu_type = arguments['type']
        category_list = Category.get_categories('uid')
        if menu_type not in category_list:
            category_list.append(menu_type)
            Category.update({'uid': uid, 'category': pickle.dumps(category_list)}, ['uid'])
        return self.is_done(result)
