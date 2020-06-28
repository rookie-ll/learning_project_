# -*- encoding: utf8 -*-
from flask import current_app, flash, redirect, url_for, render_template, request
from APP.models.gift import Gift
from APP.models.wish import Wish
from APP.webapp import web
from flask_login import login_required, current_user
from APP.webapp.extends import db
from APP.ViewsModel.wish import MyWishes
from APP.webapp.libs.email import sed_mail


@web.route('/my/wish')
@login_required
def my_wish():
    wish_of_main = Wish.get_user_wish(current_user.id)

    isbn_list = [wish.isbn for wish in wish_of_main]
    gift_count_list = Wish.get_wish_count(isbn_list)
    view_model = MyWishes(wish_of_main, gift_count_list)
    return render_template("my_wish.html", wishes=view_model.gifts)


@web.route('/wish/book/')
@login_required
def save_to_wish():
    isbn = request.args.get("isbn")
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            current_user.beans += current_app.config["BASE_NUM"]
            db.session.add(wish)
            db.session.commit()
        flash("添加成功")
    else:
        flash("这本书已经添加到赠送清单，或者已经添加到你的心愿清单，请勿重复添加！")
    return redirect(url_for("web.book_detail", isbn=isbn))

@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    """
            向想要这本书的人发送一封邮件
            注意，这个接口需要做一定的频率限制
            这接口比较适合写成一个ajax接口
        """
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书，请点击“加入到赠送清单”添加此书。添加前，请确保自己可以赠送此书')
    else:
        sed_mail(wish.user.email, '有人想送你一本书', 'email/satisify_wish.html', wish=wish,
                  gift=gift)
        flash('已向他/她发送了一封邮件，如果他/她愿意接受你的赠送，你将收到一个鱼漂')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/edraw_from_wish')
def edraw_from_wish():
    pass


@web.route('/wish/redraw_from_wish')
@login_required
def redraw_from_wish():
    isbn=request.args.get("isbn")
    wish=Wish.query.filter(Wish.isbn==isbn,Wish.launched==False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for("web.my_wish"))


@web.route('/my/wishs')
@login_required
def my_wishs():
    wish = Wish.query.filter(Wish.uid == current_user.id).all()
    count = 0
    print(wish)
    for i in wish:
        print(i.uid)
    return ""
