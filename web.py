from flask import Blueprint
from flask_login import login_required

web = Blueprint('web', __name__)


@web.route('/index')
@login_required
def index ():
    return 'hello,world'


@web.route('/personal')
@login_required
def personal ():
    return 'personal page'
