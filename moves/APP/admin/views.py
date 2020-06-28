import datetime
import os
import uuid

from APP import Admin, Tag, db, Movie, Prevaew, User, Comment, Moviecol, Oplog, Userlog, Adminlog, Auth, Role
from manager import app
from . import admin
from flask import redirect, render_template, url_for, flash, session, request, g, abort
from .forms import LoningFroms, TagsFroms, MovieForm, PreviewForm, PwdForm, AuthForm, RoleForm, AdminAddForm
from functools import wraps
from werkzeug.utils import secure_filename


# 上下文应用处理器
@admin.context_processor
def tpl_extra():
    data = dict(
        nowtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    )
    return data


@admin.before_request
def g_g():
    g.nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 访问控制
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 访问控制
def admin_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = Admin.query.join(
            Role
        ).filter(
            Admin.role_id == Role.id,
            Admin.id == session.get("admin_id")
        ).first()

        auths = admin.role.auths
        print(auths)
        auths = list(map(lambda v: int(v), auths.split(",")))
        print(auths)
        auths_list = Auth.query.all()
        print(auths_list)
        urls = [v.url for v in auths_list for val in auths if val == v.id]
        '''s=list()
        for v in auths_list:
            for val in auths:
                if val==v.id:
                    s.append(v.url)
        print("s=",end=":")
        print(s)
'''
        print(urls)
        rule = request.url_rule
        a=list()
        str(rule)
        a.append(rule)
        print(a)

        if str(rule) not in urls:
            abort(404)

        return f(*args, **kwargs)

    return decorated_function


# 文件格式
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@admin.route('/')
@admin_login_req
def index():
    return render_template("admin/index.html")


# 登陆
@admin.route('/login/', methods=["GET", "POST"])
def login():
    form = LoningFroms()
    if form.validate_on_submit():
        date = form.data
        print(date)
        admins = Admin.query.filter_by(adminname=form.data.get("admname")).first()
        # print(dir(admins))
        if not date.get("pwd") == admins.password:
            flash("密码错误")
            return redirect(url_for("admin.login"))
        session["admin"] = date.get("admname")
        session["admin_id"] = admins.id
        # print(date.get("admname"))
        adminlogin = Adminlog(
            admin_id=admins.id,
            ip=request.remote_addr
        )
        db.session.add(adminlogin)
        db.session.commit()
        print(session)
        return redirect(request.args.get("next") or url_for("admin.index"))

        # print(date)
    return render_template("admin/login.html", form=form)


# 注销
@admin.route('/logout/')
@admin_login_req
def logout():
    session.pop("admin", None)
    session.pop("admin_id", None)
    print(session)
    return redirect(url_for("admin.login"))


# 修改密码
@admin.route('/pwd/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        name = session.get("admin")
        print(name)
        admin = Admin.query.filter_by(adminname=name).first()
        if admin.password == data.get("oldpwd"):
            admin.password = data.get("newpwd")
            db.session.add(admin)
            db.session.commit()
            g.name = "wode"
            flash("修改成功,请重新登陆", "ok")
            return redirect(url_for("admin.logout"))
        flash("旧密码错误", "err")

    return render_template("admin/pwd.html", form=form)


# 标签管理
@admin.route('/tag/add/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def tag_add():
    form = TagsFroms()
    if form.validate_on_submit():
        tag_sum = Tag.query.filter_by(name=form.data.get("name")).count()
        if tag_sum == 1:
            flash("标签已经存在", "err")
            return redirect(url_for("admin.tag_add"))
        tag = Tag(

            name=form.data.get("name")
        )

        db.session.add(tag)
        db.session.commit()
        flash("添加成功", "ok")
        oplog = Oplog(
            admin_id=session.get("admin_id"),
            ip=request.remote_addr,
            reason="添加日志%s" % form.data.get("name")
        )
        db.session.add(oplog)
        db.session.commit()
        redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)


# 标签列表
@admin.route('/tag/list/<int:page>/', methods=["GET"])
@admin_login_req
def tag_list(page=None):
    if page == None:
        page = 1
    page_date = Tag.query.order_by(Tag.add_time.desc()).paginate(page=page, per_page=10)
    # print(page_date)

    return render_template("admin/tag_list.html", page_date=page_date)


# 删除标签
@admin.route('/tag/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def tag_del(id=None):
    date = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(date)
    # print(date.id)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for("admin.tag_list", page=1))


# 编辑标签
@admin.route('/tag/edit/<int:id>', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def tag_edit(id=None):
    form = TagsFroms()
    tags = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        tag_sum = Tag.query.filter_by(name=form.data.get("name")).count()
        if tags.name == form.data.get("name") and tag_sum == 1:
            flash("标签已经存在", "err")
            return redirect(url_for("admin.tag_edit", id=id))
        tags.name = form.data.get("name")

        db.session.add(tags)
        db.session.commit()
        flash("修改成功", "ok")
        return redirect(url_for("admin.tag_list", page=1))
    return render_template("admin/edit.html", form=form, tags=tags)


# 添加电影
@admin.route('/movie/add/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def movie_add():
    form = MovieForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        data = form.data
        print(data)
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], os.stat.S_IRWXO)
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config["UP_DIR"] + url)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        movie = Movie(
            title=data.get("title"),
            url=url,
            info=data.get("info"),
            logo=logo,
            star=int(data.get("star")),
            lenght=data.get("length"),
            playnum=0,
            commentnum=0,
            tag_id=int(data.get("tag_id")),
            area=data.get("area"),
            release_time=data.get("release_time"),

        )
        db.session.add(movie)
        db.session.commit()
        flash("添加成功", "ok")
        return redirect(url_for("admin.movie_add"))
    return render_template("admin/movie_add.html", form=form)


@admin.route('/movie/list/<int:page>/', methods=["GET"])
@admin_login_req
def movie_list(page=None):
    if page == None:
        page = 1
    page_data = Movie.query.join(Tag).filter(Movie.tag_id == Tag.id).order_by(Movie.add_time.desc()).paginate(page=page,
                                                                                                              per_page=1)

    return render_template("admin/movie_list.html", page_data=page_data)


# 删除电影
@admin.route('/movie/del/<int:id>', methods=["GET"])
@admin_login_req
@admin_auth
def movie_del(id=None):
    data = Movie.query.filter_by(id=id).first_or_404()
    db.session.delete(data)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for("admin.movie_list", page=1))


# 编辑电影
@admin.route('/movie/edit/<int:id>', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def movie_edit(id=None):
    form = MovieForm()
    form.logo.validators = []
    form.url.validators = []
    movies = Movie.query.get_or_404(int(id))
    if request.method == "GET":
        form.info.data = movies.info
        form.tag_id.data = movies.tag_id
        form.star.data = movies.star
    if form.validate_on_submit():
        movie_sum = Movie.query.filter_by(title=form.data.get("title")).count()

        if movie_sum == 1 and form.data.get("title") == movies.title:
            flash("电影已经存在", "err")
            return redirect(url_for("admin.movie_edit", id=movies.id))
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], os.stat.S_IRWXO)
        if form.url.data.filename != "":
            file_url = secure_filename(form.url.data.filename)
            movies.url = change_filename(file_url)
            form.url.data.save(app.config["UP_DIR"] + movies.url)

        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            movies.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + movies.logo)

        movies.title = form.data.get("title")
        movies.star = form.data.get("star")
        movies.info = form.data.get("info")
        movies.tag_id = form.data.get("tag_id")
        movies.lenght = form.data.get("length")
        movies.area = form.data.get("area")
        movies.release_time = form.data.get("release_time")
        db.session.add(movies)
        db.session.commit()
        flash("添加成功", "ok")
        return redirect(url_for("admin.movie_edit", id=movies.id))
    return render_template("admin/movie_edit.html", id=movies.id, form=form, movies=movies)


# 上映预告
@admin.route('/preview/add/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def preview_add():
    form = PreviewForm()
    data = form.data
    if form.validate_on_submit():
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], os.stat.S_IRWXO)
        logo = change_filename(file_logo)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        preview = Prevaew(
            title=data.get("title"),
            logo=logo
        )
        db.session.add(preview)
        db.session.commit()
        flash("添加成功", "ok")

    return render_template("admin/preview_add.html", form=form)


@admin.route('/preview/list/<int:page>')
@admin_login_req
def preview_list(page=None):
    if page == None:
        page = 1

    page_data = Prevaew.query.order_by(Prevaew.add_time.desc()).paginate(page=page, per_page=1)
    return render_template("admin/preview_list.html", page_data=page_data)


# 预告删除
@admin.route('/preview/del/<int:id>')
@admin_login_req
@admin_auth
def preview_del(id=None):
    preview = Prevaew.query.filter_by(id=id).first_or_404()
    db.session.delete(preview)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for("admin.preview_list", page=1))


# 预告编辑
@admin.route('/preview/edit/<int:id>', methods=["GET", "POST"])
@admin_login_req
def preview_edit(id=None):
    form = PreviewForm()
    data = form.data
    form.logo.validators = []
    preview = Prevaew.query.get(int(id))
    if form.validate_on_submit():
        preview_sum = Prevaew.query.filter(Prevaew.title == data.get("title")).count()
        if preview.title == data.get("title") and preview_sum == 1:
            flash("这条预告已经存在", "err")
            return redirect(url_for("admin.preview_list", page=1))

        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], os.stat.S_IRWXO)

        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + preview.logo)

        preview.title = data.get("title")
        db.session.add(preview)
        db.session.commit()
        flash("修改成功", "ok")
        return redirect(url_for("admin.preview_list", page=1))
    return render_template("admin/preview_edit.html", form=form, preview=preview)


# 会员管理
@admin.route('/user/list/<int:page>')
@admin_login_req
def user_list(page=None):
    if page == None:
        page = 1
    page_data = User.query.order_by(User.add_taime.desc()).paginate(page=page, per_page=1)

    return render_template("admin/user_list.html", page_data=page_data)


@admin.route('/user/view/<int:id>')
@admin_login_req
@admin_auth
def user_view(id=None):
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_view.html", user=user)


@admin.route('/user/del/<int:id>')
@admin_login_req
@admin_auth
def user_del(id=None):
    user = User.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for("admin.user_list", page=1))


# 评论列表
@admin.route('/comment/list/<int:page>')
@admin_login_req
def comment_list(page=None):
    if page == None:
        page = 1
    # page_data=Comment.query.order_by(Comment.add_time.desc()).paginate(page=page,per_page=1)
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(
        Comment.add_time.desc()
    ).paginate(page=page, per_page=1)
    print(page_data.items)
    a = page_data.items
    print(a[0].content)
    for i in page_data.items:
        print(i.user.username)
    return render_template("admin/comment_list.html", page_data=page_data)


# 收藏管理
@admin.route('/moviecol/list/<int:page>')
@admin_login_req
def moviecol_list(page=None):
    if page == None:
        page = 1
    # page_data=Moviecol.query.order_by(Moviecol.add_time.desc()).paginate(page=page,per_page=1)
    page_data = Moviecol.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Moviecol.movie_id,
        User.id == Moviecol.user_id
    ).order_by(
        Moviecol.add_time.desc()
    ).paginate(page=page, per_page=1)
    return render_template("admin/moviecol_list.html", page_data=page_data)


# 收藏编辑

# 删除收藏
@admin.route('/moviecol/list/<int:id>')
@admin_login_req
@admin_auth
def moviecol_del(id=None):
    m_del = Moviecol.query.order_by(id=id).first_or_404()
    db.session.delete(m_del)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for("admin.moviecol_list", page=1))


# 日志管理

# 操作日志
@admin.route('/oplog/list<int:page>')
@admin_login_req
@admin_auth
def oplog_list(page=None):
    if page == None:
        page = 1
    page_data = Oplog.query.join(
        Admin
    ).filter(
        Admin.id == Oplog.admin_id
    ).order_by(
        Oplog.add_time.desc()
    ).paginate(page=page, per_page=1)
    return render_template("admin/oplog_list.html", page_data=page_data)


# 管理员登陆日志
@admin.route('/adminloginlog/list<int:page>')
@admin_login_req
@admin_auth
def adminloginlog_list(page=None):
    if page == None:
        page = 1
    page_data = Adminlog.query.join(
        Admin
    ).filter(
        Admin.id == Adminlog.admin_id
    ).order_by(Adminlog.add_time.desc()).paginate(page=page, per_page=10)
    return render_template("admin/adminloginlog_list.html", page_data=page_data)


# 会员登陆日志
@admin.route('/userloginlog/list<int:page>')
@admin_login_req
@admin_auth
def userloginlog_list(page=None):
    if page == None:
        page = 1

    page_data = Userlog.query.join(
        User
    ).filter(
        User.id == Userlog.user_id
    ).order_by(Userlog.add_time.desc()).paginate(page=page, per_page=1)
    return render_template("admin/userloginlog_list.html", page_data=page_data)


# 权限管理
@admin.route('/auth/add/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def auth_add():
    form = AuthForm()
    data = form.data
    if form.validate_on_submit():
        cum = Auth.query.filter(Auth.name == data.get("auth_name") and Auth.url == data.get("auth_add")).count()
        if not cum == 1:
            auth = Auth(
                name=data.get("auth_name"),
                url=data.get("auth_add"),
            )
            db.session.add(auth)
            db.session.commit()
            flash("添加成功", "ok")
        else:
            flash("添加失败", "err")
    return render_template("admin/auth_add.html", form=form)


@admin.route('/auth/list/<int:page>')
@admin_login_req
@admin_auth
def auth_list(page=None):
    if page == None:
        page == 1
    page_data = Auth.query.order_by(Auth.add_time.desc()).paginate(page=page, per_page=10)
    return render_template("admin/auth_list.html", page_data=page_data)


# 删除权限
@admin.route('/auth/del/<int:id>')
@admin_login_req
@admin_auth
def auth_del(id):
    del_auth = Auth.query.filter_by(id=id).first_or_404()
    db.session.delete(del_auth)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for("admin.auth_list", page=1))


# 编辑权限
@admin.route('/auth/edit/<int:id>', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def auth_edit(id=None):
    form = AuthForm()
    data = form.data
    edit_auth = Auth.query.filter_by(id=id).first_or_404()
    print(edit_auth)
    if form.validate_on_submit():
        cum = Auth.query.filter(Auth.name == data.get("auth_name") and Auth.url == data.get("auth_add")).count()
        if not cum == 1:
            edit_auth.name = data.get("auth_name")
            edit_auth.url = data.get("auth_add")
            db.session.add(edit_auth)
            db.session.commit()
            flash("添加成功", "ok")
            return redirect(url_for("admin.auth_list", page=1))
        else:
            flash("添加失败", "err")
    return render_template("admin/auth_edit.html", form=form, auth=edit_auth)


# 角色管理
@admin.route('/role/add/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def role_add():
    form = RoleForm()

    if form.validate_on_submit():
        data = form.data
        print(data)
        print(data.get("auths"))
        role = Role(
            name=data.get("name"),
            auths=",".join(map(lambda v: str(v), data.get("auths")))
        )
        db.session.add(role)
        db.session.commit()
        flash("添加成功", "ok")
    return render_template("admin/role_add.html", form=form)


# 角色列表
@admin.route('/role/list/<int:page>')
@admin_login_req
def role_list(page=None):
    if page == None:
        page = 1
    page_data = Role.query.order_by(Role.add_time.desc()).paginate(page=page, per_page=1)
    return render_template("admin/role_list.html", page_data=page_data)


# 编辑角色
@admin.route('/role/edit/<int:id>', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def role_edit(id=None):
    form = RoleForm()
    role = Role.query.get_or_404(id)
    if form.validate_on_submit():
        # sum = Role.query.filter(Role.name==form.data.get("name")).count()
        if not role.name == form.data.get("name"):
            data = form.data
            role.name = data.get("name")
            role.auths = ",".join(map(lambda v: str(v), data.get("auths")))
            db.session.add(role)
            db.session.commit()
            flash("修改成功哦", "ok")
            return redirect(url_for("admin.role_list", page=1))
        else:
            flash("名字已经存在", "err")
    return render_template("admin/role_edit.html", form=form, role=role)


# 删除角色
@admin.route('/role/del/<int:id>', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def role_del(id=None):
    del_role = Role.query.get_or_404(id)
    db.session.delete(del_role)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for("admin.role_list", page=1))


# 管理员管理
@admin.route('/admin/add/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def admin_add():
    form = AdminAddForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        data = form.data
        if data.get("password") == data.get("password2"):
            # from werkzeug.security import generate_password_hash
            admin = Admin(
                adminname=data.get("adminname"),
                password=data.get("password"),
                role_id=data.get("role_id"),
                is_super=1
            )
            db.session.add(admin)
            db.session.commit()
            flash("修改成功", "ok")
        else:
            flash("俩次密码不一致", "err")
    return render_template("admin/admin_add.html", form=form)


@admin.route('/admin/list/<int:page>')
@admin_login_req
def admin_list(page=None):
    if page == None:
        page = 1
    page_data = Admin.query.order_by(Admin.add_time.desc()).paginate(page=page, per_page=1)
    return render_template("admin/admin_list.html", page_data=page_data)
