from app.extensions import db


class User(db.Model):
    __table__ = db.Table("user", db.MetaData(bind=db.engine), autoload=True)

