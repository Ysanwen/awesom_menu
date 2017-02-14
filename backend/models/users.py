# -*-coding:utf-8-*-

from .common import BaseModel
import sqlalchemy
from uuid import uuid1


@BaseModel.register_table()
class User(BaseModel):
    __column_fileds__ = {'username': sqlalchemy.String(50), 'id': sqlalchemy.String(32), 'age': sqlalchemy.Integer, 'gender': sqlalchemy.String(10)}

    def __init__(self, username, age, gender, id=str(uuid1())):
        self.username = username
        self.age = age
        self.gender = gender
        self.id = id

