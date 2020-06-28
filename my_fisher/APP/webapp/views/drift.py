from sqlalchemy import or_, desc
from APP.ViewsModel.drift import DriftCollection
from APP.models.wish import Wish
from APP.webapp.libs.email import sed_mail
from flask_login import current_user
from APP.froms.drift_form import DriftForm
from APP.models import Gift, User
from APP.models.drift import Drift
from APP.webapp import web
from flask import render_template, request, flash, redirect, url_for
from APP.ViewsModel.book import BookViewsModel
from APP.webapp.extends import db
from flask_login import login_required
from APP.webapp.libs.enums import PendingStatus


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gifts = Gift.query.get_or_404(gid)

    if current_gifts.is_yourself_gift():
        flash("这本书是你自己的，不能向自己索要书籍")
        return redirect(url_for("web.book_drift", isbn=current_gifts.isbn))
    if not current_user.can_sent_drift():
        return redirect(url_for("not_enough_beans.html", beans=current_user.beans))
    gifter = current_gifts.user.summary
    form = DriftForm(request.form)
    if request.method == "POST" and form.validate():
        save_drift(form, current_gifts)
        sed_mail(current_gifts.user.email, '有人想要一本书', 'email/get_gift.html',
                 wisher=current_user,
                 gift=current_gifts)
        return redirect(url_for('web.pending'))
    return render_template("drift.html", gifter=gifter, user_beans=current_user.beans)


@web.route('/pending')
@login_required
def pending():
    drift = Drift.query.filter(
        or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id)
    ).order_by(desc(Drift.create_time)).all()
    drifts = DriftCollection(drift, current_user.id)
    return render_template("pending.html", drifts=drifts.data)


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(Gift.id == current_user.id, Drift.id == did).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for("web.pending"))


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(id=did, requester_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for("web.pending"))


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(id=did, gifter_id=current_user.id).first_or_404()
        drift.pendin = PendingStatus.Success
        current_user.beans += 1

        gift = Gift.query.filter(Gift.id == drift.gift_id, Gift.uid == current_user.id).first_or_404()
        gift.launched = True

        wish = Wish.query.filter(
            Wish.isbn == drift.isbn, Wish.uid == drift.requester_id, Wish.launched == False
        ).get_or_404()
        wish.launched = True
        # Wish.query.filter_by(
        #     isbn=drift.isbn, uid=drift.requester_id, launched=False
        # ).update({Wish.launched: True})
    return redirect(url_for("web.pending"))


def save_drift(drift_form, current_gift):
    if current_user.beans < 1:
        # TODO 自定义异常
        raise Exception()

    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book = BookViewsModel(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        db.session.add(drift)

        current_user.beans -= 1
