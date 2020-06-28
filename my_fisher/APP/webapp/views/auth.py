# -*- encoding: utf8 -*-
from flask import render_template, request, redirect, url_for, flash, session, make_response
from APP.froms.register_form import RegisterForm, LoginForm, MailForm, ResetPasswordForm
from APP.models.user import User
from flask_login import login_user, logout_user
from APP.webapp import web
from APP.webapp.extends import db
from APP.webapp.libs.email import sed_mail


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        user = User()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
        flash("注册成功")
        return redirect(url_for("web.login"))
    return render_template("auth/register.html", form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter(User.email == form.email.data).first()
        if not user:
            flash("邮箱不正确")
        if not user.check_password(form.password.data):
            flash("密码错误")
        login_user(user, remember=True)
        n = request.args.get("next")
        if not n or not n.startswith("/"):
            return redirect(url_for("web.index"))
        else:
            return redirect(n)
    return render_template("auth/login.html", form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = MailForm(request.form)
    if request.method == "POST":
        if form.validate():
            user = User.query.filter(User.email == form.email.data).first_or_404()
            sed_mail(form.email.data, "重置密码", "email/reset_password.html", user=user, token=user.generate_token())
            flash("一封邮件已经发送，请到"+ form.email.data + "中查看")
            return redirect(url_for("web.login"))
    return render_template("auth/forget_password_request.html", form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == "GET" and form.validate():
        if User.cheage_password(token, form.password2.data):
            flash("密码修改成功")
            return redirect(url_for("web.login"))
        else:
            flash("密码修改失败")
    return render_template("auth/forget_password.html", form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    return render_template("auth/change_password.html")


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("web.index"))
