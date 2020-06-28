from flask import current_app

from app.extensions import db
from .db_base import DB_Base
from datetime import datetime


class Category(db.Model, DB_Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    # 设置与post的双向关系
    # posts = db.relationship('Post',secondary="tags_posts", back_populates='categories')
    posts = db.relationship('Posts', back_populates='categories')


# 博客模型
class Posts(db.Model, DB_Base):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), index=True)  # 博客标题
    article = db.Column(db.Text)  # 博客的内容
    visit = db.Column(db.Integer, default=0)  # 访问量
    state = db.Column(db.Integer, default=0)  # 是否所有人可见
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # 发表时间
    # 设置一对多外键
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 设置与comment的双向关系
    comments = db.relationship('Comment', back_populates='posts', cascade='all, delete-orphan')

    # 设置与category的双向关系
    # categories= db.relationship('Post', secondary="tags_posts", back_populates='posts')
    categories = db.relationship('Category', back_populates='posts')


class Comment(db.Model, DB_Base):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', back_populates='comments')

    # 外键，指向文章表的ｉｄ与文章构成一对多关系（一个文章有多个评论）
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    # 与文章的双向级联关系
    posts = db.relationship('Posts', back_populates='comments')

    # 设置回复，指向自己的ｉｄ（邻接列表）与评论构成一对多关系（一个评论有多个回复）
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    # 评论的回复：级联删除，当评论被删除的时候，所有的回复将被删除（级联删除设置在“多”这一侧）
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    # 父对象，也就是被评论的那个（相当于一篇文章）标量关系
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
