# -*-coding:utf-8-*-
from .common import ApiAction, request_method_check, Argument, parse_arguments
from flask_login import current_user
from backend.models import QrcodeMenu
import uuid
import qrcode
from backend import app
import os
from datetime import datetime


class QrcodeMenuApi(ApiAction):
    """docstring for QrcodeMenuApi"""
    @request_method_check(['GET'])
    @parse_arguments(Argument('create_quantity', int, required=True))
    def create_qrcode(self, arguments):
        quantity = arguments['create_quantity']
        uid = current_user['id']

        qrcode_list = []
        base_server_host = app.config['SERVER_HOST']
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/qrcode')
        # create qrcode and save in static/qrcode
        for i in range(quantity):
            qrcode_item = dict()
            table_id = str(uuid.uuid1())
            qr = qrcode.QRCode(
                version=2,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10, border=1)
            qrcode_link_to = base_server_host + '/mobile_index?uid=' + uid + '&table_id=' + table_id
            qr.add_data(qrcode_link_to)
            qr.make(fit=True)
            qr_img = qr.make_image()
            qr_img_name = str(uuid.uuid1()) + '.png'
            qr_img.save(os.path.join(output_dir, qr_img_name))

            qrcode_item.update(
                {'uid': uid, 'table_id': table_id,
                    'table_name': '请设置编号', 'url_address': qr_img_name,
                    'create_time': datetime.now()}
            )
            qrcode_list.append(qrcode_item)

        # save into db
        QrcodeMenu.insert_many(qrcode_list)
        result = QrcodeMenu.find(uid=uid)
        if result:
            return self.is_done(result)
        else:
            return self.is_fail('create qrcode fail!')

    @request_method_check(['GET'])
    def get_all_qrcodes(self, arguments):
        uid = current_user['id']
        result = QrcodeMenu.find(uid=uid)
        if result:
            return self.is_done(result)
        else:
            return self.is_fail('no qrcode!')

    @request_method_check(['POST'])
    @parse_arguments(
        Argument('id', str, required=True),
        Argument('table_name', str, required=True))
    def update_qrcode(self, arguments):
        id = int(arguments['id'])
        table_name = arguments['table_name']
        result = QrcodeMenu.update({'id': id, 'table_name': table_name}, ['id'])
        if result:
            new_data = QrcodeMenu.find_by_id(id)
            return self.is_done(new_data)
        else:
            return self.is_fail('update fail')
