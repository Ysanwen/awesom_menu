# -*-coding:utf-8-*-
from .common import ApiAction, request_method_check, Argument, parse_arguments
import pickle
from backend.models import Order, QrcodeMenu, Menu
from flask_login import current_user
from datetime import datetime
import pytz


class OrderApi(ApiAction):
    """
    Documnet for OrderApi
    """

    @request_method_check(['POST'])
    @parse_arguments(
        Argument('uid', str, required=True),
        Argument('table_id', str, required=True),
        Argument('table_name', str, required=True),
        Argument('menu_list', list, required=True),
        Argument('quantity_list', list, required=True),
        Argument('order_price', float, required=True))
    def create_order(self, arguments):
        # 用户创建订单

        # 初始化每个菜的状态
        menu_list = arguments['menu_list']
        quantity_list = arguments['quantity_list']
        item_status_list = pickle.dumps([Order.ItemStatus['notBegin']] * len(menu_list))
        store_menu_list = pickle.dumps(menu_list)
        store_quantity_list = pickle.dumps(quantity_list)
        arguments.update({'menu_list': store_menu_list, 'quantity_list': store_quantity_list, 'item_status_list': item_status_list})
        result = Order(**arguments).save()
        # update quantity
        Menu.update_quantity(menu_list, quantity_list)
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
        # update quantity
        Menu.update_quantity(menu_list, quantity_list)
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
                # 撤销订单时，恢复可售数量
                if(status == Order.CANCLE):
                    current_order = Order.find_one(oid=oid)
                    menu_list = pickle.loads(current_order['menu_list'])
                    quantity_list = pickle.loads(current_order['quantity_list'])
                    quantity_list = map(lambda x: -x, quantity_list)
                    Menu.update_quantity(menu_list, quantity_list)
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

    @request_method_check(['POST'])
    @parse_arguments(
        Argument('oid', str, required=True),
        Argument('payType', str, required=True),
        Argument('actualityPay', float, required=True),
        Argument('comment', str, required=True))
    def pay_order(self, arguments):
        oid = arguments['oid']
        pay_type = arguments['payType']
        actuality_paid = arguments['actualityPay']
        comment = arguments['comment']
        paid_time = datetime.now(pytz.timezone('Asia/Shanghai'))
        result = Order.update({
            'oid': oid, 'pay_type': pay_type, 'actuality_paid': actuality_paid,
            'comment': comment, 'paid_time': paid_time, 'status': Order.HASPAID}, ['oid'])
        # 更新销售量至每一个单品，后续可采用消息队列的方式完成
        try:
            find_order = Order.find_one(oid=oid)
            menu_list = pickle.loads(find_order['menu_list'])
            quantity_list = pickle.loads(find_order['quantity_list'])
            for index in range(len(quantity_list)):
                menu = menu_list[index]
                quantity = quantity_list[index]
                find_menu = Menu.find_one(id=menu['id'])
                monthly_sales = find_menu['monthly_sales'] + quantity
                Menu.update({'id': menu['id'], 'monthly_sales': monthly_sales}, ['id'])
        except Exception as e:
            pass
        return self.is_done({'paid': 'success'}) if result else self.is_fail('paid fail')

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

    @request_method_check(['GET'])
    @parse_arguments(
        Argument('currentPage', int, required=True),
        Argument('pageSize', int, required=True))
    def get_finished_orders(self, arguments):
        if not current_user.is_authenticated:
            return self.is_fail('not allowed')
        uid = current_user['id']
        currentPage = arguments['currentPage']
        pageSize = arguments['pageSize']
        offset = (currentPage - 1) * pageSize
        result = Order.find(uid=uid, _offset=offset, _limit=pageSize, return_count=True, status=Order.HASPAID)
        total = result.pop()['total']

        for item in result:
            item['menu_list'] = pickle.loads(item['menu_list'])
            item['quantity_list'] = pickle.loads(item['quantity_list'])
            item['item_status_list'] = pickle.loads(item['item_status_list'])
        return self.is_done({'data': result, 'total': total})
