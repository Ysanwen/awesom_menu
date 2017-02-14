# -*-coding:utf-8-*-

from . import view_bp
from flask import render_template


@view_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@view_bp.app_errorhandler(403)
def visit_forbidden(e):
    return render_template('403.html'), 403


@view_bp.app_errorhandler(410)
def page_gone(e):
    return render_template('410.html'), 410


@view_bp.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
