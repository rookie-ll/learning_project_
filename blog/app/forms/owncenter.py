from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, IntegerField, RadioField, PasswordField, SelectField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Length, EqualTo, Email
from flask_wtf.file import FileAllowed, FileRequired, FileField
from .posts import SendPosts
from app.models import User, Category
from app.extensions import file  # 导入文件上传配置对象


# 修改与查看个人信息的表单类
class UserInfo(FlaskForm):
    username = StringField('用户名', render_kw={'readonly': 'true'})
    sex = RadioField(label='性别', choices=[('1', '男'), ('0', '女')], validators=[DataRequired('性别必选')])
    age = IntegerField('年龄', validators=[DataRequired('年龄不能为空'), NumberRange(min=1, max=99, message='年龄在1~99之间')])
    email = StringField('邮箱', render_kw={'readonly': 'true'})
    lastLogin = StringField('上次登录时间', render_kw={'disabled': 'true'})
    register = StringField('注册时间', render_kw={'disabled': 'true'})
    submit = SubmitField('修改')


# 修改与查看个人密码邮箱的表单类
class Change_pwd_email(FlaskForm):
    password = PasswordField(
        '修改密码',
        validators=[DataRequired('密码不能为空...'),
                    Length(min=6, max=12, message='密码在6~12位之间')],
        render_kw={'placeholder': '请输入密码...'}
    )
    new_pwd = PasswordField('确认密码', validators=[DataRequired('确认密码不能为空...')],
                            render_kw={'placeholder': '请输入确认密码...'})

    email = StringField('旧邮箱', validators=[DataRequired('邮箱地址不能为空'), Email(message='请输入正确的邮箱地址')],
                        render_kw={'placeholder': '请输入邮箱'})
    new_email = StringField('新邮箱', validators=[DataRequired('邮箱地址不能为空'), Email(message='请输入正确的邮箱地址')],
                            render_kw={'placeholder': '请输入修改后的邮箱'})

    submit = SubmitField('修改')

    # 验证邮箱是否存在
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已存在 无需修改')

    # # 验证密码是否正确
    # def validate_password(self, field):
    #     if User.query.filter(
    #             User.check_password(field.data)field.data
    #     ).first():
    #         raise ValidationError('密码错误 请重新输入')


class CategoryForm(SendPosts, Form):
    add_categories = StringField(
        "添加标签",
        validators=[
            DataRequired(u"请输入地址")
        ],
        render_kw={
            "class": "form-control"
        }
    )

    # 验证标签是否存在
    def validate_add_categories(self, field):
        if Category.query.filter_by(name=field.data).first():
            # raise ValidationError('该标签已存在 请重新输入')
            return False
        return True


# # 文件上传类
class Upload(FlaskForm):
    icon = FileField(
        '头像上传',
        validators=[
            FileRequired('您还没有选择上传的头像'),
            FileAllowed(file, message='该文件类型不允许上传')
        ]
    )
    submit = SubmitField('上传')
