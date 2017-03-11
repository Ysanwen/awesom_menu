# -*-coding:utf-8-*-
from .common import ApiAction, request_method_check, Argument, parse_arguments
import pickle
from backend.models import Order


class OrderApi(ApiAction):
    """
    Documnet for OrderApi
    """

    @request_method_check(['POST'])
    @parse_arguments(
        Argument('table_id', str, required=True),
        Argument('table_name', str, required=True),
        Argument('menu_list', list, required=True),
        Argument('quantity_list', list, required=True),
        Argument('order_price', float, required=True))
    def create_order(self, arguments):
        menu_list = pickle.dumps(arguments['menu_list'])
        quantity_list = pickle.dumps(arguments['quantity_list'])
        arguments.update({'menu_list': menu_list, 'quantity_list': quantity_list})
        result = Order(**arguments).save()
        return self.is_done('order success') if result else self.is_fail('order fail')
