from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Email, length, ValidationError, EqualTo
from APP.models import User


class RegisterForm(Form):
    email = StringField(
        validators=[
            DataRequired(),
            length(8, 64),
            Email("message='email不符合规范'")
        ]
    )
    password = PasswordField(
        validators=[
            DataRequired(message='密码不可以为空，请输入密码'),
            length(6, 32)
        ]
    )
    nickname = StringField(
        validators=[
            DataRequired(),
            length(2, 10, message='昵称至少需要2个字符，最多10个字符')
        ]
    )

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已经被注册")

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError("用户名已经被注册")


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), length(8, 64), Email(message='email不符合规范')])

    password = PasswordField(validators=[DataRequired(message='密码不可以为空，请输入密码'), length(6, 32)])


class MailForm(Form):
    email = StringField(validators=[DataRequired(), length(8, 64), Email(message='email不符合规范')])


class ResetPasswordForm(Form):
    password1 = PasswordField(
        validators=[
            DataRequired(),
            length(6, 32)
        ]
    )
    password2 = PasswordField(
        validators=[
            DataRequired(),
            length(6, 32),
            EqualTo(password1, message="俩次密码竟不相同?")
        ]
    )
