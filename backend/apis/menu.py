# -*-coding:utf-8-*-
from .common import ApiAction, request_method_check, Argument, parse_arguments
from flask_login import current_user
import pickle
from backend.models import Menu

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
        return self.is_done(result)
