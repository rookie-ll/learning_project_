import uuid

from APP import User, db, Userlog, Movie, Prevaew, Tag, Comment, Moviecol
from APP.home.forms import RegisterForm
from . import home
from flask import render_template, url_for, redirect, flash, request, session
from functools import wraps


def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("username"):
            return redirect(url_for("home.logins", next=request.url))
        return f(*args, **kwargs)

    return decorated_function



@home.route('/home/')
def homes():
    return render_template("home/home.html")


# 登陆
@home.route('/login/', methods=["GET", "POST"])
def logins():
    if request.method == 'GET':
        return render_template("home/login.html")
    if request.method == "POST":
        password = request.form.get("password")
        contact = request.form.get("contact")
        sum = User.query.filter(User.username == contact).count()
        if sum == 1:
            users = User.query.filter(User.username == contact).first()
            print(users)
            if users.username == contact and users.password == password:
                session["username"] = contact
                session["user_id"] = users.id
                # flash("登陆成功", "ok")
                userlog = Userlog(
                    user_id=session.get("user_id"),
                    ip=request.remote_addr
                )
                db.session.add(userlog)
                db.session.commit()
                return redirect(url_for("home.user"))
            else:
                flash("用户名或者密码不正确", "err")
        else:
            flash("用户不存在", "err")
        print(password)
        print(contact)

    return render_template("home/login.html")


# 注销
@home.route('/loginout/')
@admin_login_req
def loginout():
    if session.get("username"):
        session.pop("username")
        session.pop("user_id")
        flash("您已成功退出，请重新登陆", "ok")
    else:
        flash("您还没有登陆，请登陆", "err")
        redirect(url_for("home.logins"))
    return redirect(url_for("home.logins"))


# 注册
@home.route('/regist/', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        data = form.data
        sum = User.query.filter(User.username == data.get("username")).count()
        sum2 = User.query.filter(User.phone == data.get("phone")).count()
        sum3 = User.query.filter(User.emial == data.get("email")).count()

        if not (sum == 1) and not (sum2 == 1) and not (sum3 == 1):
            if data.get("password") == data.get("rpassword"):
                user = User(
                    username=data.get("username"),
                    password=data.get("password"),
                    emial=data.get("email"),
                    phone=data.get("phone"),
                    uuid=uuid.uuid4().hex
                )
                db.session.add(user)
                db.session.commit()
                flash("注册成功", "ok")
                return redirect(url_for("home.logins"))
            else:
                flash("俩次密码不一致", "err")
        else:
            flash("表单中有重复项目", "err")
    return render_template("home/regist.html", form=form)


# 用户
@home.route('/user/', methods=["GET", "POST"])
@admin_login_req
def user():
    user_id = session.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if request.method == "GET":
        return render_template("home/user.html", user=user)
    if request.method == "POST":
        username = request.form.get("name")
        emial = request.form.get("email")
        phone = request.form.get("phone")
        if user and emial and phone:
            user.username = username
            user.emial = emial
            user.phone = phone
            user.face = request.form.get("face")
            user.info = request.form.get("info")
            db.session.add(user)
            db.session.commit()
            flash("修改成功", "ok")
        else:
            flash("用户名，邮箱，电话不可以为空", "err")
    return render_template("home/user.html", user=user)


# 密码
@home.route('/pwd/', methods=["GET", "POST"])
@admin_login_req
def pwd():
    if request.method == "GET":
        return render_template("home/pwd.html")
    if request.method == "POST":
        logings_user = User.query.filter_by(id=session.get("user_id")).first()

        if request.form.get("oldpwd") == logings_user.password:
            if request.form.get("newpwd"):
                logings_user.password = request.form.get("newpwd")
                db.session.add(logings_user)
                db.session.commit()
                flash("修改成功", "ok")
            else:
                flash("密码不能为空", "err")
        else:
            flash("旧密码错误", "err")

    return render_template("home/pwd.html")


# 评论记录
@home.route('/comments/<int:page>/')
@admin_login_req
def comments(page=None):
    if page == None:
        page = 1
    page_data = Comment.query.filter(Comment.user_id == session.get("user_id")).paginate(page=page, per_page=5)
    return render_template("home/comments.html", page_data=page_data)


# 登陆日志
@home.route('/loginlog/<int:page>')
@admin_login_req
def loginlog(page=None):
    if page == None:
        page = 1
    page_data = Userlog.query.join(
        User
    ).filter(
        User.id == session.get("user_id"),
        Userlog.user_id == User.id
    ).paginate(page=page, per_page=5)
    return render_template("home/loginlog.html", page_data=page_data)


# 评论记录
# 电影添加
@home.route('/moviecol/add/')
@admin_login_req
def moviecol_add():
    uid = request.args.get("uid", "")
    mid = request.args.get("mid", "")
    moviecol = Moviecol.query.filter(Moviecol.movie_id == mid, Moviecol.user_id == uid).count()
    if moviecol == 1:
        data = dict(ok=0)
    if moviecol == 0:
        moviecol = Moviecol(
            movie_id=mid,
            user_id=uid,
        )
        db.session.add(moviecol)
        db.session.commit()
        data = dict(ok=1)

    import json
    return json.dumps(data)


# 电影收藏
@home.route('/moviecol/<int:page>/')
@admin_login_req
def moviecol(page=None):
    if page == None:
        page = 1

    page_data = Moviecol.query.filter(Moviecol.user_id == session.get("user_id")).paginate(page=page, per_page=5)

    return render_template("home/moviecol.html", page_data=page_data)


@home.route("/")
def indexs():
    return redirect(url_for("home.index", page=1))


# 主页
@home.route('/<int:page>')
def index(page=None):
    if page == None:
        page = 1
    tags = Tag.query.all()
    page_data = Movie.query
    tid = request.args.get("tid", 0)

    if int(tid) != 0:
        page_data = page_data.filter(Movie.tag_id == tid)

    star = request.args.get("star", 0)
    if int(star) != 0:
        page_data = page_data.filter(Movie.star == star)

    time = request.args.get("time", 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(Movie.add_time.desc())
        elif int(time) == 2:
            page_data = page_data.order_by(Movie.add_time.asc())

    pm = request.args.get("pm", 0)
    if int(pm) != 0:
        if int(pm) == 1:
            page_data = page_data.order_by(Movie.playnum.desc())
        elif int(pm) == 2:
            page_data = page_data.order_by(Movie.playnum.asc())

    cm = request.args.get("cm", 0)
    if int(cm) != 0:
        if int(cm) == 1:
            page_data = page_data.order_by(Movie.commentnum.desc())
        elif int(cm) == 2:
            page_data = page_data.order_by(Movie.commentnum.asc())

    page_data = page_data.paginate(page=page, per_page=1)

    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm
    )
    print(page_data.items)
    return render_template("home/index.html", tags=tags, p=p, page_data=page_data)


# 轮播图
@home.route('/anamation/')
def anamation():
    data = Prevaew.query.all()
    # print(page_data)
    print()
    return render_template("home/anamation.html", data=data)


# 搜索
@home.route('/search/<int:page>/')
def search(page=None):
    if page == None:
        page = 1
    key = request.args.get("key", "")
    page_data = Movie.query.filter(
        Movie.title.ilike("%" + key + "%")
    ).order_by(
        Movie.add_time.desc()
    ).paginate(page=page, per_page=1)
    num = len(page_data.items)
    print(num)
    page_data.key=key

    return render_template("home/search.html", key=key, page_data=page_data, num=num)


# 评论页面
@home.route('/play/<int:id>/<int:page>/', methods=["GET", "POST"])
def play(id=None, page=None):
    if page == None:
        page = 1
    page_data = Comment.query.filter(Comment.movie_id == id).order_by(Comment.add_time.desc()).paginate(page=page,
                                                                                                        per_page=10)
    print(page_data.items)
    num = len(Comment.query.all())
    movie = Movie.query.get_or_404(id)

    if request.method == "GET":
        movie.playnum = movie.playnum + 1
        db.session.add(movie)
        db.session.commit()
        return render_template("home/play.html", movie=movie, page_data=page_data)
    if request.method == "POST":

        if request.form.get("comment") and session.get("username"):
            comment = Comment(
                content=request.form.get("comment"),
                movie_id=id,
                user_id=session.get("user_id")
            )
            db.session.add(comment)
            db.session.commit()
            movie.commentnum = movie.commentnum + 1
            db.session.add(movie)
            db.session.commit()
        else:
            flash("请登陆以后再来评论", "err")
        page_data = Comment.query.filter(Comment.movie_id == id).order_by(Comment.add_time.desc()).paginate(page=page,
                                                                                                            per_page=10)
        print(page_data.items)
    return render_template("home/play.html", movie=movie, page_data=page_data, num=num)
