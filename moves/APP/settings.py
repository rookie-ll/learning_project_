import os


class Config(object):
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:123456@127.0.0.1:3306/mouve"
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SECRET_KEY="LASDKJFＬjfalsfaslkdfj344"
    UP_DIR=os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/uploads/")