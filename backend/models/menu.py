# -*-coding:utf-8-*-

from .common import BaseModel
import sqlalchemy
from datetime import datetime
import pickle
import pytz


@BaseModel.register_table(primary_id='id', primary_type='Integer')
class Menu(BaseModel):
    ONSELL = 0
    OFFSELL = 1
    MonthlySales = 0
    __column_fileds__ = {
        'uid': sqlalchemy.String,
        'name': sqlalchemy.String(50),
        'type': sqlalchemy.String,
        'unit': sqlalchemy.String,
        'price': sqlalchemy.Float,
        'quantity': sqlalchemy.Integer,
        'monthly_sales': sqlalchemy.Integer,
        'url_address': sqlalchemy.PickleType,
        'status': sqlalchemy.Integer,
        'create_time': sqlalchemy.DateTime
    }

    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid', None)
        self.name = kwargs.get('name', None)
        self.type = kwargs.get('type', None)
        self.unit = kwargs.get('unit', None)
        self.price = kwargs.get('price', None)
        self.quantity = kwargs.get('quantity', None)
        self.monthly_sales = Menu.MonthlySales
        self.url_address = kwargs.get('url_address', None)
        self.status = kwargs.get('status', None) if kwargs.get('status', None) else Menu.ONSELL
        self.create_time = datetime.now(pytz.timezone('Asia/Shanghai'))

    @classmethod
    def update_quantity(cls, menu_list, quantity_list):
        for index in range(len(menu_list)):
            menu_id = menu_list[index]['id']
            menu_item = cls.find_one(id=menu_id)
            quantity_item = quantity_list[index]
            new_quantity = menu_item['quantity'] - quantity_item
            cls.update({'id': menu_id, 'quantity': new_quantity}, ['id'])


@BaseModel.register_table(primary_id='id', primary_type='Integer')
class Category(BaseModel):
    """docstring for MenuItemType"""
    __column_fileds__ = {
        'uid': sqlalchemy.String,
        'category': sqlalchemy.PickleType,
    }

    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid', None)
        self.category = kwargs.get('category', None)

    @classmethod
    def get_categories(cls, uid):
        result = cls.find_one(uid=uid)
        if result:
            return pickle.loads(result['category'])
        else:
            return []
