# -*-coding:utf-8-*-
from .common import ApiAction, request_method_check, Argument, parse_arguments
from flask_login import current_user
import pickle
from backend.models import Menu, Category


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


class CategoryApi(ApiAction):
    """docstring for CategoryApi"""
    @request_method_check(['GET'])
    @parse_arguments(Argument('uid', str, required=True))
    def get_categories_menu(self, arguments):
        uid = arguments['uid']
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
