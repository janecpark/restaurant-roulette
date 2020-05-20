from flask import Flask, Blueprint, render_template

error = Blueprint('error', __name__, template_folder='templates')


@error.app_errorhandler(500)
def handle500(e):
    """ Return error 500 """
    return render_template('/error/500.html'), 500


@error.app_errorhandler(404)
def handle404(e):
    """ Return error 404 """
    return render_template('/error/404.html'), 404

@error.app_errorhandler(400)
def handle400(e):
    """ Return error 404 """
    return render_template('/error/400.html'), 400