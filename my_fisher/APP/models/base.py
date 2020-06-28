from sqlalchemy import Column, SmallInteger, DateTime
from datetime import datetime
from APP.webapp.extends import db


class Base(db.Model):
    __abstract__ = True
    status = Column(SmallInteger, default=1)
    create_time = Column(DateTime, default=datetime.now)

    # def __init__(self):
    #     super().__init__()
    #     self.create_time = datetime.utcnow()
    def delete(self):
        self.status = 0

    # 体现python动态语言的特性  将dict中与db中有相同key时，写入db
    def set_attrs(self, attr_dice):
        for key, value in attr_dice.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)
