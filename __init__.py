from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('flaskr.secure')
    app.config.from_object('flaskr.setting')

    from flaskr.models.base import db
    db.init_app(app)
    db.create_all(app=app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登陆'

    mail.init_app(app)

    register_blueprint(app)

    return app


def register_blueprint(app):
    # from flaskr.spider_homeword.homeword1 import homeword
    # app.register_blueprint(homeword)

    from flaskr.auth import auth
    app.register_blueprint(auth)

    from flaskr.web import web
    app.register_blueprint(web)
