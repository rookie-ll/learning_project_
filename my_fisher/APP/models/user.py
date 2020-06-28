from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from math import floor
from APP.models.gift import Gift
from APP.models.wish import Wish
from APP.models.drift import Drift
from APP.webapp.libs.search_lib import isbn_or_key
from APP.webapp.libs.yushu_book import YuShuBook
from APP.webapp.libs.enums import PendingStatus
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from APP.models.base import Base
from APP.webapp.extends import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from APP.webapp.extends import loginmanager


class User(UserMixin, Base):
    # __tablename__ = 'base' 对默认表名进行更改
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=False)  # db中的密码不能用明文，要加密
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return "密码不能被你看到哦"

    @password.setter
    def password(self, password):
        """
        密码加密
        :param password:
        :return:
        """
        self._password = generate_password_hash(password)

    def check_password(self, password):
        """
        密码比对
        :param password:
        :return:
        """
        return check_password_hash(self._password, password)

    def generate_token(self, out_time=300):
        """
        生成token
        :param out_time:
        :return:
        """
        s = Serializer(current_app.config.get("SECRET_KEY"), out_time)
        s.dumps({"id": self.id}).decode("utf-8")
        return s

    @staticmethod
    def cheage_password(token, password):
        """
        验证token，并且修改password
        :param token:
        :param password:
        :return:
        """
        s = Serializer(current_app.config.get("SECRET_KEY"))
        try:
            data = s.loads(token.encode("utf-8"))
        except Exception as e:
            return False
        with db.auto_commit():
            user = User.query.get(data.get("id"))
            if user is None:
                return False
            user.password = password

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_counter=str(self.send_counter) + "/" + str(self.receive_counter)
        )

    def can_sent_drift(self):
        """
        判断鱼豆是否大于等于一，而且每索取俩本书必须送出一本书
        :return:
        """
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        success_recevie_count = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.Success).count()
        return True if floor(success_recevie_count / 2) <= floor(success_gifts_count) else False

    def can_save_to_list(self, isbn):
        """
        判断能否添加到心愿清单和礼物清单
        :param isbn:
        :return:
        """
        if isbn_or_key(isbn) != "isbn":
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False

        # 即不在心愿清单又不在赠送清单才能添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False


@loginmanager.user_loader
def get_user(user_id):
    """
    这是flask—login需要获得一个当前用户的id
    :param user_id:
    :return:
    """
    return User.query.get(int(user_id))
