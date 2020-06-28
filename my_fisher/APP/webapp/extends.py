from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


class SQLAlchemy(_SQLAlchemy):
    from contextlib import contextmanager
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()  # 回滚事务
            raise e


db = SQLAlchemy()
migrate = Migrate()
loginmanager = LoginManager()
mail = Mail()


def ext_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
    loginmanager.init_app(app)
    mail.init_app(app)

    loginmanager.session_protection = "strong"
    loginmanager.login_view = "web.login"
    loginmanager.login_message = "请登陆"
