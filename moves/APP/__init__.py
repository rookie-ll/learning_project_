from flask import Flask, render_template

from APP.ext import init_ext
from .models import *


def create_app():
    app = Flask(__name__)

    # 初始化配置
    from .settings import Config
    app.config.from_object(Config)

    # 注册蓝图
    from APP.admin import admin
    from APP.home import home
    app.register_blueprint(blueprint=home)
    app.register_blueprint(blueprint=admin, url_prefix='/admin')

    # 初始化第三方插件
    init_ext(app)

    # 404页面
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("home/404.html")

    return app
