# -*-coding:utf-8-*-

from .views_blueprint import view_bp
from flask import render_template

@view_bp.route('/')
def index():
    # return 'hello world!'
    return render_template('index.html')

@view_bp.route('say/<string:s>')
def say(s):
    if s == 'yes':
        return 'awesome!'
    else:
        return 'you said {s}'.format(s=s)
