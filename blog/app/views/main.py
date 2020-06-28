from flask import Blueprint, render_template, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Posts

main = Blueprint('main', __name__)

# @main.route("/test")
# def test_E():
#     from app.models.flask_sqlalchemy_test import User
#     data=User.query.all()
#     return str(data)

# 首页视图
@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    if page == None:
        page = 1
    # 查询pid为0并且所有人可见的博客  pid不为0 证明是评论和回复的内容  按照时间的降序显示
    pagination = Posts.query.filter(
        Posts.state == 0
    ).order_by(
        Posts.timestamp.desc()
    ).paginate(page, current_app.config['PAGE_NUM'])
    data = pagination.items  # 获取page页面的数据
    return render_template('main/index.html', posts=data, pagination=pagination)

