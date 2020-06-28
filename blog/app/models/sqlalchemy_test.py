from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root:123456@192.168.40.1:3306/blog")
# 定义模型类继承的父类和数据库会话
# 定义执行查询语句，提交事务的实例
dbsession = sessionmaker(bind=engine)
db = scoped_session(dbsession)  # 线程安全
# 自动加载表结构
md = MetaData(engine)
# 用于模型类的继承
Base = declarative_base()


class User(Base):
    __table__ = Table("user", md, autoload=True)


if __name__ == '__main__':
    data = db.query(User).all()
    print(data)
