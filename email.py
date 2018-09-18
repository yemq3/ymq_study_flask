import logging
from threading import Thread
from flask import current_app, render_template
from flaskr import mail
from flask_mail import Message


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            logging.exception(e)


def send_mail(to, subject, template, **kwargs):
    '''
    :param to: 收件邮箱
    :param subject: 邮件标题
    :param template: 邮件模版
    '''
    msg = Message(subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
