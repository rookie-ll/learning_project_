from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request, jsonify
from app.forms import SendPosts, Comment  # 导入发表博客与评论回复表单类
from app.models import Posts, Category, Comment as Comments  # 导入博客模型类
from flask_login import login_required, current_user
from sqlalchemy import or_  # 导入或查询

posts = Blueprint('posts', __name__)


# 发表博客
@posts.route('/send_posts/', methods=['GET', 'POST'])
@login_required
def send_posts():
    form = SendPosts()
    # 判断登录后在进行发表
    if not current_user.is_authenticated:
        flash('您还没有登录  请登录后在发表')
    elif form.validate_on_submit():
        # 保存发表博客的数据
        Posts(
            title=form.title.data,
            article=form.article.data,
            user=current_user,
            category_id=form.categories.data
        ).save()
        flash('博客发表成功')
        return redirect(url_for('main.index'))
    return render_template('posts/send_posts.html', form=form)



# 博客搜索
@posts.route('/search/', methods=['GET', 'POST'])
def search():
    try:
        page = request.args.get('page', 1, type=int)
    except:
        page = 1
    # 获取搜索的关键字
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        print(keyword)
    else:
        keyword = request.args.get('keyword', '')
    # 查询pid为0并且所有人可见的博客  pid不为0 证明是评论和回复的内容  按照时间的降序显示
    pagination = Posts.query.filter(
        or_(
            Posts.title.ilike("%" + keyword + "%"),
            Posts.article.ilike("%" + keyword + "%")
        ),
        Posts.state == 0
    ).order_by(
        Posts.timestamp.desc()
    ).paginate(page, current_app.config['PAGE_NUM'])
    data = pagination.items  # 获取page页面的数据
    return render_template('posts/search_detail.html', pagination=pagination, posts=data, keyword=keyword)


# 博客详情
@posts.route('/posts_detail/')
def posts_detail():
    # 查询当前博客的内容 pid为博客的自增id 并不是博客模型字段的pid
    pid = request.args.get("pid")
    page = request.args.get("page", 1, type=int)
    p = Posts.query.get(pid)
    p.visit += 1  # 博客的访问量
    p.save()
    form = Comment()  # 发表评论和回复的表单类
    # 查询出博客的评论内容和回复 按照博客内容和回复在一起的排序顺序  过滤条件为博客的path宏包含博客id 的 这样就将博客的内容过滤了出去  只查询评论和回复的内容
    pagedata = Comments.query.filter(
        Comments.post_id == p.id
    ).order_by(Comments.timestamp.desc()).paginate(page, current_app.config['PAGE_NUM'])
    return render_template('posts/posts_detail.html', posts=p, form=form, comment=pagedata)


# 评论
@posts.route('/comment/', methods=["GET", "POST"])
@login_required
def comment():
    form = Comment()
    if form.validate_on_submit():
        page = request.form.get("page", 1, type=int)
        pid = request.form.get("pid", type=int)
        count = request.form.get("content")
        uid = current_user.id
        Comments(
            count=count,
            post_id=pid,
            user_id=uid
        ).save()
    return redirect(url_for("posts.posts_detail", pid=pid, page=page))


# 回复
@posts.route('/reply/', methods=['GET', 'POST'])
@login_required
def reply():
    page = request.form.get("page", 1, type=int)
    form = Comment()
    if form.validate_on_submit():
        pid = request.form.get('pid', type=int)
        rid = request.form.get('rid', type=int)
        count = request.form.get("content")
        uid = current_user.id
        Comments(
            count=count,
            post_id=pid,
            user_id=uid,
            replied_id=rid,
        ).save()
    return redirect(url_for('posts.posts_detail', pid=pid, page=page))


# 处理博客收藏与取消收藏的操作
@posts.route('/do_favorite/')
def do_favorite():
    try:
        # 获取ajax传递过来的pid
        pid = request.args.get('pid', type=int)
        # 判断是否收藏了
        if current_user.is_favorite(pid):
            # 调用取消收藏
            current_user.delete_favorite(pid)
        else:
            # 调用执行收藏
            current_user.add_favorite(pid)
        return jsonify({'res': 200})
    except:
        return jsonify({'res': 500})
