# -*-coding:utf-8-*-

from .common import BaseModel
import sqlalchemy
from datetime import datetime
import uuid
import pickle
import pytz


@BaseModel.register_table(primary_id='id', primary_type='Integer')
class Order(BaseModel):
    # 订单状态
    CANCLE = -1
    NOTPAID = 0
    HASPAID = 1
    # 订单内每个菜的状态
    ItemStatus = {'notBegin': '未开始制作', 'onProcess': '制作中', 'finished': '制作完成'}
    """docstring for Order"""
    __column_fileds__ = {
        'oid': sqlalchemy.String,
        'table_id': sqlalchemy.String,
        'table_name': sqlalchemy.String,
        'menu_list': sqlalchemy.PickleType,
        'quantity_list': sqlalchemy.PickleType,
        'item_status_list': sqlalchemy.PickleType,
        'order_price': sqlalchemy.Float,
        'actuality_paid': sqlalchemy.Float,
        'create_time': sqlalchemy.DateTime,
        'paid_time': sqlalchemy.DateTime,
        'status': sqlalchemy.Integer,
        'comment': sqlalchemy.String,
        'pay_type': sqlalchemy.String,
        'uid': sqlalchemy.String
    }

    def __init__(self, **kwargs):
        self.oid = str(uuid.uuid1())
        self.table_id = kwargs.get('table_id', None)
        self.table_name = kwargs.get('table_name', None)
        self.menu_list = kwargs.get('menu_list', None)
        self.quantity_list = kwargs.get('quantity_list', None)
        self.item_status_list = kwargs.get('item_status_list', None)
        self.order_price = kwargs.get('order_price', None)
        self.actuality_paid = kwargs.get('actuality_paid', 0)
        self.create_time = datetime.now(pytz.timezone('Asia/Shanghai'))
        self.paid_time = kwargs.get('paid_time', datetime.now(pytz.timezone('Asia/Shanghai')))
        self.status = kwargs.get('status', Order.NOTPAID)
        self.comment = kwargs.get('comment', '')
        self.pay_type = kwargs.get('pay_type', '')
        self.uid = kwargs.get('uid', '')

    @classmethod
    def get_current_order(cls, table_id):
        data = {}
        result = cls.find_one(table_id=table_id, status=cls.NOTPAID)

        if result:
            data.update({
                'menu_list': pickle.loads(result['menu_list']),
                'quantity_list': pickle.loads(result['quantity_list']),
                'item_status_list': pickle.loads(result['item_status_list'])})
        else:
            data.update({'menu_list': [], 'quantity_list': []})
        return data
