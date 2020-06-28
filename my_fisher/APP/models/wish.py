from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship


from APP.models.base import Base
from APP.webapp.extends import db
from APP.webapp.libs.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        """
        返回一本书籍的原始数据
        :return:
        """
        yushu = YuShuBook()
        yushu.search_by_isbn(self.isbn)
        return yushu.first

    @classmethod
    def get_user_wish(cls, uid):
        """
        礼物列表
        :return:
        """
        wish_list = Wish.query.filter_by(uid=uid, launched=False).all()
        return wish_list

    @classmethod
    def get_wish_count(cls, isbn_list):
        """
        根具传入的一组isbn,到wish中计算出礼物的心愿数量
        :return:
        """
        from APP.models import Gift
        count_list = db.session.query(
            func.count(Gift.id),
            Gift.isbn
        ).filter(
            Gift.launched == False, Gift.status == 1, Gift.isbn.in_(isbn_list)
        ).group_by(Gift.isbn).all()
        # count_list = [CountList(w[0], w[1]) for w in count_list]
        count_list = [{"isbn": w[0], "count": w[1]} for w in count_list]
        return count_list

