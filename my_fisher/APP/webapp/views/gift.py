# -*- encoding: utf8 -*-
from flask import current_app, flash, redirect, url_for, render_template, request
from APP.webapp.libs.enums import PendingStatus
from APP.models.drift import Drift
from APP.models.gift import Gift
from APP.webapp import web
from flask_login import login_required, current_user
from APP.webapp.extends import db
from APP.ViewsModel.gift import MyGifts


@web.route('/my/gifts')
@login_required
def my_gifts():
    gift_of_main = Gift.get_user_gift(current_user.id)

    isbn_list = [gift.isbn for gift in gift_of_main]
    wish_count_list = Gift.get_wish_count(isbn_list)
    view_model = MyGifts(gift_of_main, wish_count_list)
    return render_template("my_gifts.html", gifts=view_model.gifts)


@web.route('/gifts/book/')
@login_required
def save_to_gifts():
    isbn = request.args.get("isbn")
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift(
                uid=current_user.id,
                isbn=isbn
            )
            current_user.beans += current_app.config["BASE_NUM"]
            db.session.add(gift)
        flash("添加成功")
    else:
        flash("这本书已经添加到赠送清单，或者已经添加到你的心愿清单，请勿重复添加！")
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    gift = Gift.query.filter(Gift.launched == False, Gift.id == gid).first_or_404()
    drift=Drift.query.filter(Drift.gift_id==gift.id,Drift.pending==PendingStatus.Waiting).first_or_404()
    if drift:
        flash("请先到鱼鳔中取消相关操作")
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config["BASE_NUM"]
            gift.delete()
    return redirect(url_for("web.my_gifts"))
