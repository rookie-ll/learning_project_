from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func

from APP.models.base import Base
from APP.models.wish import Wish
from APP.webapp.extends import db
from APP.webapp.libs.yushu_book import YuShuBook
from collections import namedtuple

CountList = namedtuple("ContList", ["isbn", "count"])


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu = YuShuBook()
        yushu.search_by_isbn(self.isbn)
        return yushu.first

    def is_yourself_gift(self, uid):
        """
        判断是否是自己的礼物
        :param uid:
        :return:
        """
        return True if self.uid == uid else False

    @classmethod
    def get_user_gift(cls, uid):
        """
        礼物列表
        :return:
        """
        gift_list = Gift.query.filter_by(uid=uid, launched=False).all()
        return gift_list

    @classmethod
    def get_wish_count(cls, isbn_list):
        """
        根具传入的一组isbn,到wish中计算出礼物的心愿数量
        :return:
        """
        count_list = db.session.query(
            func.count(Wish.id),
            Wish.isbn
        ).filter(
            Wish.launched == False, Wish.status == 1, Wish.isbn.in_(isbn_list)
        ).group_by(Wish.isbn).all()
        # count_list = [CountList(w[0], w[1]) for w in count_list]
        count_list = [{"isbn": w[0], "count": w[1]} for w in count_list]
        return count_list

    # 对象代表一个礼物
    # 类代表礼物这个事务，是一个抽象，不是一个具体的礼物
    @classmethod
    def recent(cls):
        """
        返回没有送出去的最近上传礼物
        :return:
        """
        # 链式调用
        # 主函数query
        # 子函数filter,all
        gift = Gift.query.filter_by(
            launched=False
        ).order_by(
            desc(Gift.create_time)
        ).limit(30).distinct().all()
        return gift
