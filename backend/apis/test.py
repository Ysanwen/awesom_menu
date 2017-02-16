# -*-coding:utf-8-*-

from .common import ApiAction, request_method_check, Argument, parse_arguments
from backend.models import User


class TestApi(ApiAction):
    @request_method_check(['POST'])
    @parse_arguments(
        Argument('mobile', str, default='not know', required=False),
        Argument('password', str, default=0, required=True))
    def create_user(self, arguments):
        user = User(arguments['mobile'], arguments['password'])
        result = user.save()
        return self.is_done(result)

    @request_method_check(['GET'])
    @parse_arguments(Argument('id', str, required=True))
    def get_user(self, arguments):
        user = User.find_by_id(arguments['id'])
        return self.is_done(user)

    @request_method_check(['GET'])
    def get_all(self, arguments):
        all_data = User.find()
        return self.is_done(all_data)
