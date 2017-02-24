# -*- coding:utf-8 -*-

from flask import jsonify, request
from functools import wraps
from flask_restful import Resource


class ApiAction(Resource):
    """
    rewrite the dispatch_request to deal with api request,
    and add some common function
    """
    methods = ['POST', 'GET', 'DELETE', 'PUT']

    def dispatch_request(self, *args, **kwargs):
        action = kwargs.get('action', None)
        if action is None:
            return jsonify({'error': 'no api_action called'})
        else:
            call_action = getattr(self, action, None)
            if call_action:
                return call_action(self.extract_arguments())
            else:
                return jsonify({'error': 'no this api interface'})

    def extract_arguments(self):
        arguments = dict()
        arguments.update(request.args.to_dict())
        arguments.update(request.form.to_dict())
        arguments.update(request.files.to_dict())
        return arguments

    def is_done(self, data):
        if isinstance(data, dict) or isinstance(data, str) or isinstance(data, list) or isinstance(data, bool):
            return jsonify({'success': True, 'data': data})
        else:
            raise Exception("data type error!")

    def is_fail(self, message):
        if isinstance(message, str):
            return jsonify({'success': False, 'message': message})
        else:
            raise Exception("data type error!")


def request_method_check(request_method_list):
    """
    request_method_list shoud contains one or more of 'get','put'
    'delete','post','update'
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.method in request_method_list or request.method.upper() in request_method_list:
                return f(*args, **kwargs)
            else:
                return jsonify({'error': 'the request method error'})
        return wrapper
    return decorator


class ApiError(Exception):
    code = 1044

    def __init__(self, message):
        self.message = message


class Argument(object):
    """
    :param name:string type, the key of arguments pass to action
    :param text_type: int,str,bool,datetime,etc
    :param default: default value of argument
    :param required:bool,default is True
    """
    def __init__(self, name, text_type, default=None, required=True):
        self.name = name
        self.text_type = text_type
        self.default = default
        self.required = required

    def verify_argument(self, argument):
        if type(argument) == self.text_type:
            return True
        else:
            try:
                self.text_type(argument)
                return True
            except ValueError:
                return False


def parse_arguments(*ars):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            new_arguments = dict()
            arguments = args[1]
            argument_key = arguments.keys()
            for item in ars:
                if item.required and item.name not in argument_key:
                    if type(item.default) == item.text_type:
                        new_arguments[item.name] = item.default
                    else:
                        return jsonify({'default param error': 'the type of {0} should be {1}'.format(item.default, item.text_type)})
                else:
                    if item.name in argument_key:
                        if item.verify_argument(arguments[item.name]):
                            new_arguments[item.name] = item.text_type(arguments[item.name])
                        else:
                            return jsonify({'param error': 'the type of {0} should be {1}'.format(item.name, item.text_type)})
            args = tuple([args[0], new_arguments])
            return f(*args, **kwargs)
        return wrapper
    return decorator
