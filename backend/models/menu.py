# -*-coding:utf-8-*-

from .common import BaseModel
import sqlalchemy
from datetime import datetime


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
        self.create_time = datetime.now()
