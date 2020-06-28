from flask import Flask
from app.views import register_blueprint  # 导入views注册蓝本对象的方法
from app.config import configDict  # 导入配置类的字典
from .extensions import init_app  # 导入初始化扩展库的init_app方法
from app.models import Posts,Category,Comment,User


# 加载整个App项目并返回App对象
def create_app(configName='default'):
    app = Flask(__name__)
    # 加载配置类
    app.config.from_object(configDict[configName])
    # 注册蓝本
    register_blueprint(app)
    # 初始化扩展库
    init_app(app)
    # 添加自定义模板过滤器
    addTemFilter(app)
    return app


# 自定义模板过滤器
def addTemFilter(app):
    # 内容超出给定的长度 显示...
    def showEllipsis(Str, length=30):
        if len(Str) > length:
            Str = Str[0:length] + '...'
        return Str

    # 获取回复人的名称的过滤器
    def replayName(pid):
        username = Posts.query.get(int(pid)).user.username
        return username

    app.add_template_filter(showEllipsis)
    app.add_template_filter(replayName)
