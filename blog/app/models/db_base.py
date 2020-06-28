from app.extensions import db


# 自定义封装模型基类
class DB_Base:
    # 添加一条数据
    def save(self):
        with db.auto_commit():
            db.session.add(self)

    # 添加多条数据
    @staticmethod
    def save_all(*args):
        with db.auto_commit():
            db.session.add_all(args)

    # 删除
    def delete(self):
        with db.auto_commit():
            db.session.delete(self)
