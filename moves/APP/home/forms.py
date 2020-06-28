from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import DataRequired,ValidationError,Email,Regexp
from flask_wtf import FlaskForm


# 注册表单
from APP import User


class RegisterForm(FlaskForm):
    username = StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称")
        ],
        description="昵称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "昵称"
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱"),
            Email("邮箱格式不正确")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "邮箱"
        }
    )
    phone = StringField(
        label="手机",
        validators=[
            DataRequired("请输入手机号"),
            Regexp("1[34578]\\d[10]",message="手机格式不正确")

        ],
        description="手机",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "手机"
        }
    )
    password = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "密码"
        }
    )
    rpassword = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请再次输入密码"),
            #EqualTo(password,message="俩次密码不一致！")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "确认密码"
        }
    )
    submit = SubmitField(
        "注册",
        render_kw={
            "class": "btn btn-lg btn-success btn-block"
        }
    )

    def validata_name(self,field):
        name=field.data
        sum=User.query.filter_by(username=name).count()
        if sum==1:
            raise ValidationError("用户名已存在")

    def validata_email(self,field):
        email=field.data
        sum=User.query.filter_by(emial=email).count()
        if sum==1:
            raise ValidationError("用户名已存在")

    def validata_name(self,field):
        phone=field.data
        sum=User.query.filter_by(phone=phone).count()
        if sum==1:
            raise ValidationError("用户名已存在")

