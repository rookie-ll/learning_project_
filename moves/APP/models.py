from datetime import datetime

from .ext import db

class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    username=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))
    emial=db.Column(db.String(100),unique=True)
    phone=db.Column(db.String(11),unique=True)
    info=db.Column(db.Text(100))
    face=db.Column(db.String(255))#头像
    add_taime=db.Column(db.DateTime,index=True,default=datetime.now())
    uuid=db.Column(db.String(255),unique=True)
    userloges=db.relationship("Userlog",backref="user")
    comments=db.relationship("Comment",backref="user")#评论的反向关系
    moviecols=db.relationship("Moviecol",backref="user")#与收藏的反向关系
    def __repr__(self):
        return "<Userlog %r>"%self.username

#会员登陆日志
class Userlog(db.Model):
    ''''''
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    ip=db.Column(db.String(100))
    add_time=db.Column(db.DateTime,index=True,default=datetime.now())


    def __repr__(self):
        return "<Userlog %r>"%self.id

#标签
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)#编号
    name=db.Column(db.String(100))#标题
    add_time = db.Column(db.DateTime, index=True, default=datetime.now())
    movies=db.relationship("Movie",backref="tag")
    def __repr__(self):
        return "<Tag %r>" % self.name

#电影
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title=db.Column(db.String(255),unique=True)#标题
    url=db.Column(db.String(255),unique=True)#地址
    info=db.Column(db.Text)#简介
    logo=db.Column(db.String(255),unique=True)#封面
    star=db.Column(db.SmallInteger)#星级
    playnum=db.Column(db.BigInteger)#播放量
    commentnum=db.Column(db.BigInteger)#评论
    tag_id=db.Column(db.Integer,db.ForeignKey("tag.id"))#所属标签
    area=db.Column(db.String(255))#上映地区
    release_time=db.Column(db.Date)#上映时间
    lenght=db.Column(db.String(100))#播放时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.now())#添加时间
    comments=db.relationship("Comment",backref="movie")#评论的反向关系
    moviecol=db.relationship("Moviecol",backref="movie")#与收藏的反向关系
    def __repr__(self):
        return "<Movie %r"%self.title

class Prevaew(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    add_time = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间

    def __repr__(self):
        return "<Prevaew %r>"%self.title


#评论
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    content=db.Column(db.Text)
    movie_id= db.Column(db.Integer, db.ForeignKey("movie.id"))
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return "<Comment %r>"%self.id

#电影收藏
class Moviecol(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    movie_id=db.Column(db.Integer,db.ForeignKey("movie.id"))#所属电影
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))#所属用户
    add_time = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return "<Moviecol %r>"%self.id


#权限
class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),unique=True)
    url=db.Column(db.String(255),unique=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return "<Auth %r>"%self.name


#角色
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    auths=db.Column(db.String(600))#角色权限列表
    add_time = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return "<ROle %r>"%self.name

#管理员
class Admin(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    adminname = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    is_super=db.Column(db.SmallInteger)
    role_id=db.Column(db.Integer,db.ForeignKey("role.id"))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now())
    adminlogs=db.relationship("Adminlog",backref="admin")#管理员登陆日志外键关系映射
    oplogs=db.relationship("Oplog",backref="admin")
    role=db.relationship("Role",backref="admin")
    def __repr__(self):
        return "<Admin %r>" % self.adminname

    def check_pwd(self,password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self,password,password)

#管理员登陆日志
class Adminlog(db.Model):
    ''''''
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    admin_id=db.Column(db.Integer,db.ForeignKey("admin.id"))
    ip=db.Column(db.String(100))
    add_time=db.Column(db.DateTime,index=True,default=datetime.now())


    def __repr__(self):
        return "<Adminlog %r>"%self.id


#管理员操作日志
class Oplog(db.Model):
    ''''''
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    admin_id=db.Column(db.Integer,db.ForeignKey("admin.id"))
    ip=db.Column(db.String(100))#登陆ｉｐ
    reason=db.Column(db.String(600))#操作原因
    add_time=db.Column(db.DateTime,index=True,default=datetime.now())


    def __repr__(self):
        return "<Oplog %r>"%self.id


if __name__=="__main__":
    pass
