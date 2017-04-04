# -*-coding:utf-8-*-
import os
import json
import uuid
from .common import ApiAction, request_method_check, Argument, parse_arguments
from flask_login import current_user
from flask import request
import pickle
from backend.models import Menu, Category, QrcodeMenu, Order


class MenuApi(ApiAction):
    """
    get all the menu of current user
    """
    @request_method_check(['GET'])
    def get_all_menus(self, arguments):
        uid = current_user['id']
        result = Menu.find(uid=uid)
        if result:
            for item in result:
                item['url_address'] = pickle.loads(item['url_address'])
                item['status'] = "热销中" if item['status'] == Menu.ONSELL else "未上架"
                item['monthly_sales'] = item['monthly_sales'] if item['monthly_sales'] else 0
        else:
            result = []
        return self.is_done(result)

    @request_method_check(['POST'])
    @parse_arguments(
        Argument('id', int, required=True),
        Argument('name', str, required=True),
        Argument('unit', str, required=True),
        Argument('type', str, required=True),
        Argument('price', float, required=True),
        Argument('quantity', int, required=True),
        Argument('status', int, required=True),
        Argument('new_url_list', str, required=True))
    def update_menu(self, arguments):
        file_dict = request.files.to_dict()
        new_url_list = arguments['new_url_list']
        new_url_list = json.loads(new_url_list)
        del arguments['new_url_list']
        if file_dict:
            # 保存文件后，更新new_url_list
            for k, v in file_dict.items():
                if v.mimetype.split('/')[0] != 'image':
                    return self.is_fail('upload file type is not image')
            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/upload')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            url_list = []
            for key, file in file_dict.items():
                suffix = file.filename.split('.')[-1]
                filename = str(uuid.uuid1()) + '.' + suffix
                file.save(os.path.join(output_dir, filename))
                url_list.append(filename)
            new_url_list.extend(url_list)
            arguments['url_address'] = pickle.dumps(new_url_list)
            result = Menu.update(arguments, ['id'])
        else:
            arguments['url_address'] = pickle.dumps(new_url_list)
            result = Menu.update(arguments, ['id'])
        return self.is_done({'update': 'success'}) if result else self.is_fail('update fail')


class CategoryApi(ApiAction):
    """docstring for CategoryApi"""
    @request_method_check(['GET'])
    @parse_arguments(
        Argument('uid', str, required=True),
        Argument('table_id', str, required=True))
    def get_categories_menu(self, arguments):
        uid = arguments['uid']
        table_id = arguments['table_id']
        category_list = Category.get_categories(uid)
        # if no category,create it
        if not category_list:
            new_ca = Category(**{'uid': uid, 'category': pickle.dumps([])})
            new_ca.save()
        before_ca_len = len(category_list)
        result = {}
        menu_list = Menu.find(uid=uid)
        if menu_list:
            for item in menu_list:
                if item['status'] == Menu.ONSELL:
                    item['status'] = "热销中"
                    item['monthly_sales'] = item['monthly_sales'] if item['monthly_sales'] else 0
                    item['url_address'] = pickle.loads(item['url_address'])
                    if item['type'] in result:
                        result[item['type']].append(item)
                    else:
                        result[item['type']] = []
                        result[item['type']].append(item)
                    if item['type'] not in category_list:
                        category_list.append(item['type'])
            result['category'] = category_list
        else:
            result = {'category': category_list, 'menus': menu_list}

        # add table info
        table_info = QrcodeMenu.find_one(table_id=table_id, uid=uid)
        result['table'] = table_info

        # add current_order_info
        order_info = Order.get_current_order(table_id)
        result['order_info'] = order_info

        # if category has changed,need to update
        if len(category_list) != before_ca_len:
            Category.update({'uid': uid, 'category': pickle.dumps(category_list)}, ['uid'])
        return self.is_done(result)

    @request_method_check(['POST'])
    @parse_arguments(
        Argument('uid', str, required=True),
        Argument('category', list, required=True))
    def update_category(self, arguments):
        uid = arguments['uid']
        category = arguments['category']
        Category.update({'uid': uid, 'category': pickle.dumps(category)}, ['uid'])
        result = Category.get_categories(uid)
        return self.is_done(result)
