from flask import render_template, Blueprint, request, redirect, url_for, flash
from flaskr.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from flaskr.models.base import db
from flaskr.models.user import User
from flask_login import login_user, logout_user, current_user
from .helper import *

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
        # confirm email
        from flaskr.email import send_mail
        send_mail(form.email.data, '确认邮箱',
                  'email/activate.html', user=user,
                  token=user.generate_token(86400))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('next')
            if not next or not is_safe_url(next):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))


@auth.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first()
            if user:
                from flaskr.email import send_mail
                send_mail(form.email.data, '重置密码',
                          'email/reset_password.html', user=user,
                          token=user.generate_token())
                flash('一封邮件已发送到邮箱' + account_email + ', 请查收')
            else:
                flash('账号不存在')
    return render_template('auth/forget_password_request.html',form=form)


@auth.route('/reset/password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('密码已更新')
            return redirect(url_for('auth.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/reset_password.html',form=form)

@auth.route('/confirm/<token>')
def confirm_email(token):
    success = User.confirm_email(token)
    if success:
        flash('已成功验证邮箱')
        return redirect(url_for('auth.login'))
    else:
        flash('邮箱验证失败')
    return render_template('auth/confirm.html')
