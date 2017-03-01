# -*-coding:utf-8-*-

from .common import BaseModel
import sqlalchemy
from datetime import datetime


@BaseModel.register_table(primary_id='id', primary_type='Integer')
class QrcodeMenu(BaseModel):
    """docstring for QrcodeMenu"""
    __column_fileds__ = {
        'uid': sqlalchemy.String,
        'table_name': sqlalchemy.String,
        'table_id': sqlalchemy.String,
        'url_address': sqlalchemy.String,
        'create_time': sqlalchemy.DateTime
    }

    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid', None)
        self.table_name = kwargs.get('table_name', None)
        self.table_id = kwargs.get('table_id', None)
        self.url_address = kwargs.get('url_address', None)
        self.create_time = datetime.now()
