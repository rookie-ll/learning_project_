from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy  # ORM模型扩展库
from flask_migrate import Migrate  # 模型迁移
from flask_mail import Mail  # 邮件发送扩展库
from flask_login import LoginManager  # pip install flask-login 处理用户登录的第三方扩展库
from flask_moment import Moment  # 格式化时间显示的扩展库
# 导入头像上传
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


# 实例化
bootstrap = Bootstrap()  # bootstrap扩展库
db = SQLAlchemy()  # ORM模型扩展库
migrate = Migrate()  # 模型迁移
mail = Mail()  # 邮件发送
login_manger = LoginManager()  # 处理登陆的第三方扩展库
moment = Moment()  # 实例化格式化时间显示的扩展库

file = UploadSet('photos', IMAGES)


# 加载app
def init_app(app):
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    mail.init_app(app)
    moment.init_app(app)

    login_manger.init_app(app)
    login_manger.login_view = 'user.login'  # 当你没有登录访问了需要登录的路由的时候 进行登录的端点
    login_manger.login_message = '您还没有登录 请登陆后在访问'  # 提示信息
    login_manger.session_protection = 'strong'  # 设置session的保护级别

    # # 配置文件上传
    configure_uploads(app, file)
    patch_request_class(app, size=None)



