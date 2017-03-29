# -*-coding:utf-8-*-
from .common import ApiAction, request_method_check, Argument, parse_arguments
import pickle
from backend.models import Order, QrcodeMenu
from flask_login import current_user


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
        # 用户创建订单

        # 初始化每个菜的状态
        menu_list = arguments['menu_list']
        item_status_list = pickle.dumps([Order.ItemStatus['notBegin']] * len(menu_list))
        menu_list = pickle.dumps(menu_list)
        quantity_list = pickle.dumps(arguments['quantity_list'])
        arguments.update({'menu_list': menu_list, 'quantity_list': quantity_list, 'item_status_list': item_status_list})
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
        # 用户追加订单
        table_id = arguments['table_id']
        menu_list = arguments['menu_list']
        quantity_list = arguments['quantity_list']
        order_price = arguments['order_price']

        find_order = Order.find_one(table_id=table_id, status=Order.NOTPAID)

        if not find_order:
            return self.is_fail('fail update!')
        oid = find_order['oid']
        item_status_list = pickle.loads(find_order['item_status_list'])
        item_status_list.extend([Order.ItemStatus['notBegin']] * len(menu_list))

        arguments['quantity_list'] = pickle.loads(find_order['quantity_list'])
        arguments['quantity_list'].extend(quantity_list)
        arguments['menu_list'] = pickle.loads(find_order['menu_list'])
        arguments['menu_list'].extend(menu_list)

        order_price = find_order['order_price'] + order_price
        arguments.update({
            'menu_list': pickle.dumps(arguments['menu_list']),
            'quantity_list': pickle.dumps(arguments['quantity_list']),
            'order_price': order_price, 'oid': oid, 'item_status_list': pickle.dumps(item_status_list)})
        result = Order.update(arguments, ['oid'])
        if result:
            return self.is_done({'update': 'success'})
        else:
            return self.is_fail('update error!')

    @request_method_check(['POST'])
    @parse_arguments(
        Argument('oid', str, required=True),
        Argument('operation', str, required=True),
        Argument('status', int, required=False),
        Argument('menu_list', list, required=False),
        Argument('quantity_list', list, required=False),
        Argument('item_status_list', list, required=False))
    def modify_order(self, arguments):
        # 管理员修改订单状态
        oid = arguments['oid']
        operation = arguments['operation']
        if operation == 'status':
            status = arguments.get('status', None)
            if status and status in [Order.CANCLE, Order.HASPAID, Order.NOTPAID]:
                result = Order.update({'oid': oid, 'status': status}, ['oid'])
                return self.is_done({'modify': 'success'}) if result else self.is_fail('update error!')
            else:
                return self.is_fail('status is not right')
        elif operation == 'menu_list':
            menu_list = arguments.get('menu_list', None)
            quantity_list = arguments.get('quantity_list', None)
            if menu_list and quantity_list:
                result = Order.update({'oid': oid, 'menu_list': pickle.dumps(menu_list), 'quantity_list': pickle.dumps(quantity_list)}, ['oid'])
                return self.is_done({'modify': 'success'}) if result else self.is_fail('update error!')
            else:
                return self.is_fail('error params: no menu_list or quantity_list')
        elif operation == 'item_status':
            item_status_list = arguments.get('item_status_list', None)
            if item_status_list:
                result = Order.update({'oid': oid, 'item_status_list': pickle.dumps(item_status_list)}, ['oid'])
                return self.is_done({'modify': 'success'}) if result else self.is_fail('update error!')
            else:
                return self.is_fail('error params: no item_status_list')
        else:
            return self.is_fail('unknow operation')

    @request_method_check(['GET'])
    # 管理员获取全部进行中订单
    def get_all_orders(self, arguments):
        if not current_user.is_authenticated:
            return self.is_fail('not allowed')
        uid = current_user['id']
        qrcode_tables = QrcodeMenu.find(uid=uid)
        table_list = []
        for item in qrcode_tables:
            table_list.append(item['table_id'])
        # get all the order in table_list
        orders = []
        for table_id in table_list:
            order_item = Order.find_one(table_id=table_id, status=Order.NOTPAID)
            if order_item:
                order_item['menu_list'] = pickle.loads(order_item['menu_list'])
                order_item['quantity_list'] = pickle.loads(order_item['quantity_list'])
                order_item['item_status_list'] = pickle.loads(order_item['item_status_list'])
                orders.append(order_item)
        return self.is_done(orders)
