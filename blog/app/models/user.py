from app.extensions import db  # 导入模型对象
from .db_base import DB_Base  # 导入自定义模型基类
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # 导入生成与验证密码的方法
from itsdangerous import TimedJSONWebSignatureSerializer as Seralize  # 导入序列化的方法
from flask import current_app
from flask_login import UserMixin  # 包含了判断是否登录等等方法属性的类
from app.extensions import login_manger
from .posts import Posts


# User 模型类
class User(UserMixin, db.Model, DB_Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 自增ID
    username = db.Column(db.String(12), index=True, unique=True)  # 用户名
    password_hash = db.Column(db.String(128))  # 密码 密文
    is_admin = db.Column(db.Boolean, default=False)
    sex = db.Column(db.Boolean, default=True)  # 性别
    age = db.Column(db.Integer, default=18)  # 年龄 默认18
    email = db.Column(db.String(50), unique=True)  # 邮箱
    icon = db.Column(db.String(70), default='default.png')  # 头像 默认为default.jpg
    lastLogin = db.Column(db.DateTime)  # 上次登录时间
    registerTime = db.Column(db.DateTime, default=datetime.utcnow)  # 注册时间
    confirm = db.Column(db.Boolean, default=False)  # 激活状态 默认未激活（需要发送邮件进行激活）

    # 设置模型引用关系
    """
    Posts 建立引用关系的模型
    backref 是给关联的模型  添加一个查询的属性 叫user
    lazy  加载的时机 返回查询集(可以添加连贯操作) 如果不给lazy属性值 默认则为select模式(一旦调用posts 则返回的为数据  那么就不能在进行连贯操作 添加其它过滤器)
    """
    posts = db.relationship('Posts', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', back_populates='user',lazy='dynamic', cascade='all, delete-orphan')
    # 建立多对多
    """
    secondary 多对多模型指定查询数据的中间表
    u.favorites.all()  查询用户对象u收藏了哪些博客
    p.users.all()  查询博客都被谁收藏了
    """
    favorites = db.relationship('Posts', secondary='collections', backref=db.backref('users', lazy='dynamic'),
                                lazy='dynamic')

    # 密码加密处理的装饰器
    @property
    def password(self):
        raise AttributeError("密码怎么能直接看呢")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检验密码正确性的方法
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成token 用于账户激活(也就是知道是哪个用户过来激活的)
    def generate_token(self):
        s = Seralize(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})  # 返回加密后的字符串

    # 检测传递过来的token值  进行账户的激活
    @staticmethod
    def check_token(token):
        s = Seralize(current_app.config['SECRET_KEY'])
        try:
            id = s.loads(token).get("id")
            u = User.query.get(id)
            if not u:
                return False
            u.confirm = True
            u.save()
            return True
        except:
            return False

    # 判断是否收藏的方法
    def is_favorite(self, pid):
        posts = self.favorites.all()  # 查询当前用户的所有收藏
        for p in posts:
            if p.id == pid:
                return True
        return False

    # 收藏
    def add_favorite(self, pid):
        self.favorites.append(Posts.query.get(int(pid)))
        db.session.commit()

    # 取消收藏
    def delete_favorite(self, pid):
        self.favorites.remove(Posts.query.get(int(pid)))
        db.session.commit()


# 这是一个回调方法  实时获取当前表中用户数据的对象
@login_manger.user_loader
def user_loader(uid):
    return User.query.get(int(uid))
