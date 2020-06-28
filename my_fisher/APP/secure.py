class Secures():
    DEBUG = True
    SECRET_KEY = "lksadjfSAKDLFJ2F332"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@192.168.40.1:3306/yushubook"
    # SQLALCHEMY_DATABASE_URI="mysql://username:password@server/db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # sqlalchemy 连接池
    SQLALCHEMY_POOL_SIZE = 15
    # 邮件配置
    MAIL_SERVER: "smtp.qq.com"
    MAIL_PORT: 456
    MAIL_USE_TLS: True
    MAIL_USE_SSL: False
    MAIL_USERNAME: "2593676491@qq.com"
    MAIL_PASSWORD: "kjxkkeblhgiaeced"
