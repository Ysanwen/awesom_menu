# -*-coding:utf-8-*-

from flask import has_request_context
from backend import db
# from uuid import uuid1
# from backend import app


class BaseModel(dict):
    """
    new models should extend from BaseModel
    __column_fileds__={'name':String,'age':Integer}
    """
    __column_fileds__ = {}

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    @staticmethod
    def register_table(table_name=None, primary_id='id', primary_type='String'):
        """
        decorator of cls,to auto create table
        """
        def decorator(cls):
            if has_request_context():
                if table_name:
                    _table_name = table_name
                    cls.__table_name = table_name
                else:
                    _table_name = cls.__name__.lower()
                new_table = db.get_table(_table_name, primary_id=primary_id, primary_type=primary_type)
                if not cls.__column_fileds__:
                    raise Exception('no column fileds defined!')
                if sorted(cls.__column_fileds__.keys()) != sorted(new_table.columns):
                    key_list = cls.__column_fileds__.keys()
                    map(new_table.create_column, key_list, [cls.__column_fileds__[k] for k in key_list])
            return cls
        return decorator

    @classmethod
    def get_table(cls):
        if getattr(cls, '__table_name', None) is None:
            return db.get_table(cls.__name__.lower())
        else:
            return db.get_table(cls.__table_name)

    @classmethod
    def get_columns(cls):
        return cls.get_table().cloumns

    @classmethod
    def create_column(cls, name, column_type):
        cls.get_table().create_column(name, column_type)

    @classmethod
    def create_index(cls, columns, name=None, **kwargs):
        cls.get_table().create_index(columns, name, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        result = cls.get_table().find_one(*args, **kwargs)
        if result:
            return dict(result)
        else:
            return None

    @classmethod
    def find(cls, *args, **kwargs):
        _limit = kwargs.pop('_limit', None) or kwargs.pop('limit', None)
        _offset = kwargs.pop('_offset', 0) or kwargs.pop('offset', None)
        _step = kwargs.pop('_step', 5000) or kwargs.pop('step', 5000)
        return_count = kwargs.pop('return_count', None)
        if return_count:
            total = cls.get_table().count(*args, **kwargs)
            kwargs.update({'_limit': _limit, '_offset': _offset, '_step': _step})
            result = cls.get_table().find(*args, **kwargs)
            result = [dict(item) for item in result]
            result.append({'total': total})
            return result
        else:
            kwargs.update({'_limit': _limit, '_offset': _offset, '_step': _step})
            result = cls.get_table().find(*args, **kwargs)
            if result:
                return [dict(item) for item in result]
            else:
                return None

    @classmethod
    def find_by_id(cls, id):
        result = cls.get_table().find_one(id=id)
        if result:
            return dict(result)
        else:
            return None

    @classmethod
    def insert_one(cls, data_dict, keys_list):
        result = cls.get_table().insert_ignore(data_dict, keys_list)
        return True if result else False

    @classmethod
    def insert_many(cls, data_source_list):
        return cls.get_table().insert_many(data_source_list)

    @classmethod
    def update(cls, data_dict, match_keys_list):
        return cls.get_table().update(data_dict, match_keys_list)

    def save(self, keys_list=['id']):
        new_row = dict()
        for key in self.__column_fileds__:
            if getattr(self, key, None) is None:
                raise Exception('the name of {} is not defined!'.format(key))
            else:
                new_row.update({key: getattr(self, key)})
        return self.insert_one(new_row, keys_list)
