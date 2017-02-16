# -*-coding:utf-8-*-

from .views_blueprint import view_bp
from flask import render_template, request, redirect, jsonify, session
from backend.models.users import User, load_user
from flask_login import login_user, logout_user, current_user
from backend import login_manager


@view_bp.route('/')
def index():
    # return 'hello world!'
    return render_template('index.html')


@view_bp.route('api/sign_in', methods=['POST'])
def sign_in():
    data_form = request.json
    mobile = data_form.get('mobile', None)
    password1 = data_form.get('password1', None)
    if mobile and password1:
        user = User.find_one(mobile=str(mobile))
        if user and user['isActive'] and User.validate_login(user['password'], password1):
            user = load_user(user['id'])
            login_user(user, remember=True)

            return jsonify({"success": True, 'message': 'login allowed', 'current_user': dict(current_user)})
        else:
            return jsonify({"success": False, "message": "mobile or password not correct"})
    else:
        return jsonify({"success": False, "message": "mobile or password must not be null"})


@view_bp.route('api/sign_up', methods=['POST'])
def sign_up():
    data_form = request.json
    mobile = data_form.get('mobile', None)
    password1 = data_form.get('password1', None)
    password2 = data_form.get('password2', None)
    verify_code = data_form.get('verify_code', None)
    if mobile and password1 and password2 and verify_code:
        if password1 != password2:
            return jsonify({"success": False, "message": "password is not correct"})
        if verify_code != int(session.get(str(mobile), None)):
            return jsonify({"success": False, "message": "verify_code is not correct"})
        if User.find_one(mobile=str(mobile)):
            return jsonify({"success": False, "message": "mobile is already exist"})
        user = User(mobile, password1)
        user.save()
        login_user(load_user(user.id), remember=True)
        return jsonify({"success": True, 'message': 'sign up allowed', 'current_user': dict(current_user)})
    else:
        return jsonify({"success": False, "message": "data form is not correct"})


@view_bp.route('api/sign_out', methods=['GET'])
def sign_out():
    logout_user()
    return redirect('/')


login_manager.login_view = 'views.index'
