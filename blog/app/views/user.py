from flask import Blueprint,render_template,flash,redirect,url_for
from app.forms import Register,Login,AgainActive  # 导入表单注册类
from app.models import User  # 导入User模型类
from app.email import send_mail  # 导入发送邮件函数
from flask_login import login_required,logout_user,login_user,current_user
from datetime import datetime

user = Blueprint('user',__name__)
"""
# 注册步骤
1. 创建模型类
2. 加载flask-migrate扩展库（迁移）
3. 在视图函数中导入模型类
4. 验证（用户名、邮箱）是否存在
5. 获取模板前台传递过来的数据
6. 存储
7. 明文密码变成密文密码(加密存储)
8. 配置发送邮件扩展库和功能
9. 发送邮件
10. 消息闪现（注册成功 前去激活...）
"""
@user.route('/register/',methods=['GET','POST'])
def register():
    # 实例化注册表单类
    form = Register()
    if form.validate_on_submit():
        # 实例化存储注册表单数据
        u = User(
            username=form.username.data,
            password=form.userpass.data,
            email=form.email.data
        )
        u.save()
        # 调用获取生成token的方法
        token = u.generate_token()
        # 发送邮件激活
        send_mail('账户激活',form.email.data,username=form.username.data,token=token)
        flash('注册成功 前去邮箱进行激活')
        # 成功去登录
        return redirect(url_for('user.login'))
    return render_template('user/register.html',form=form)


# 进行账户激活的视图
@user.route('/active/<token>/')
def active(token):
    if User.check_token(token):
        flash('激活成功 请前去登录...')
        # 激活成功跳转到登录
        return redirect(url_for('user.login'))
    else:
        flash('激活失败  请重新进行账户激活操作...')
        return redirect(url_for(''))


# 再次激活的视图
@user.route('/again_active/',methods=['GET','POST'])
def again_active():
    form = AgainActive()
    if form.validate_on_submit():
        u = User.query.filter(User.username == form.username.data).first()
        # print(u)
        if not u:
            flash("请输入争取的用户名或密码...")
        elif not u.check_password(form.userpass.data):
            flash('请输入正确的用户名或密码')
        elif not u.confirm:
            # 调用获取生成token的方法
            token = u.generate_token()
            # 发送邮件激活
            send_mail('账户激活',u.email, username=form.username.data, token=token)
            flash('激活邮件发送成功 前去邮箱进行激活')
        else:
            flash('该账户已经激活 请前去登录...')
    return render_template('user/again_active.html',form=form)

"""
登录的步骤
1 接受表单传递过来的数据
2 查询用户名的对象
3 如果不存在则 提示
4 判断是否激活状态
5 判断密码(错误给出提示)
6 登录成功进行处理
7 登录失败 给出提示
"""
# 登录视图
@user.route('/login/',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        u = User.query.filter(User.username == form.username.data).first()
        if not u:
            flash('请输入正确的用户名或密码')
        elif not u.confirm:
            flash('您还没有激活 请前去激活账户')
            return redirect(url_for('user.again_active'))
        elif not u.check_password(form.userpass.data):
            flash('请输入正确的用户名或密码')
        else:
            flash('登录成功')
            # 修改登录时间
            u.lastLogin = datetime.now()
            u.save()
            login_user(u,remember=form.remember.data) # 使用第三方扩展库处理登录状态的维持
            return redirect(url_for('main.index'))

    return render_template('user/login.html',form=form)



# 退出登录
@user.route('/logout/')
def logout():
    logout_user()
    flash('退出成功！')
    return redirect(url_for('main.index'))

