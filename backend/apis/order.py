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

    @request_method_check(['POST'])
    @parse_arguments(
        Argument('table_id', str, required=True),
        Argument('table_name', str, required=True),
        Argument('menu_list', list, required=True),
        Argument('quantity_list', list, required=True),
        Argument('order_price', float, required=True))
    def update_order(self, arguments):
        table_id = arguments['table_id']
        menu_list = arguments['menu_list']
        quantity_list = arguments['quantity_list']
        order_price = arguments['order_price']

        find_order = Order.find_one(table_id=table_id, status=Order.NOTPADI)

        if not find_order:
            return self.is_fail('fail update!')
        oid = find_order['oid']

        arguments['quantity_list'] = pickle.loads(find_order['quantity_list'])
        arguments['quantity_list'].extend(quantity_list)
        arguments['menu_list'] = pickle.loads(find_order['menu_list'])
        arguments['menu_list'].extend(menu_list)

        order_price = find_order['order_price'] + order_price
        arguments.update({
            'menu_list': pickle.dumps(arguments['menu_list']),
            'quantity_list': pickle.dumps(arguments['quantity_list']),
            'order_price': order_price, 'oid': oid})
        result = Order.update(arguments, ['oid'])
        if result:
            return self.is_done({'update': 'success'})
        else:
            return self.is_fail('update error!')
