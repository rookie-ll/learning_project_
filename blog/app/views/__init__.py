from .main import main  # 导入main蓝本对象
from .user import user  # 导入user蓝本对象
from .posts import posts  # 导入posts博客处理的蓝本对象
from .owncenter import owncenter  # 导入个人中心的蓝本对象

# 循环迭代的蓝本配置
blueprint_config = [
    (main,''),
    (user,''),
    (posts,''),
    (owncenter,''),
]

# 注册蓝本对象的函数
def register_blueprint(app):
    # 循环迭代注册蓝本
    for blueprint,perfix in blueprint_config:
        app.register_blueprint(blueprint,url_prefix=perfix)