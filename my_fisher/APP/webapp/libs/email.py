from APP.webapp.extends import mail
from flask_mail import Message
from flask import current_app, render_template
from threading import Thread


def send_async_email(app, msg):
    # 手动把app_context推入栈中
    with app.app_context():
        try:
            msg.send()
        except Exception as e:
            raise e


def sed_mail(to, subject, template, **kwargs):
    msg = Message(
        subject, sender=current_app.config.get("MAIL_USERNAME"), recipients=[to]
    )
    msg.html = render_template(template, **kwargs)
    # 获取flask核心对象
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
