from sqlalchemy import Column, Integer, String,Text

from APP.models.base import Base
from APP.webapp.extends import db


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, default="未名")
    author = Column(String(200))
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(Text)
    images = Column(String(50))
