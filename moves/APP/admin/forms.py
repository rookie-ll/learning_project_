from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError,EqualTo

from APP import Admin, Tag, Auth, Role


# 登陆标签
class LoningFroms(FlaskForm):
    admname = StringField(
        label="帐号",
        validators=[
            DataRequired("请输入帐号！")
        ],
        description="帐号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            # "required": "required"

        }
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            # "required": "required"

        }
    )

    submit = SubmitField(
        "登陆",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_admname(self, field):
        admname = field.data
        admin = Admin.query.filter_by(adminname=admname).count()
        if admin == 0:
            raise ValidationError("帐号不存在")


# 标签表单
tags = Tag.query.all()


class TagsFroms(FlaskForm):
    name = StringField(
        label="名称",
        validators=[
            DataRequired("请输入标签！")
        ],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！"
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 添加电影表单
class MovieForm(FlaskForm):
    title = StringField(
        label="片名",
        validators=[
            DataRequired("请输入片名！")
        ],
        description="片名",
        render_kw={
            "class": "form-control",
            # "id": "input_title",
            "placeholder": "请输入片名！"
        }
    )
    url = FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件")
        ],
        description="文件"
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": "10",
            # "id": "input_info"
        }
    )
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面")
        ],
        description="封面"
    )
    star = SelectField(
        label="星级",
        validators=[
            DataRequired("请选择星级")
        ],
        description="星级",
        coerce=int,
        choices=[(1, "１星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        render_kw={
            "class": "form-control",
            # "id": "input_tag_id"
        },
        # coerce=int
    )

    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签")
        ],
        description="标签",
        coerce=int,

        choices=[(v.id, v.name) for v in tags],
        render_kw={
            "class": "form-control",
            # "id": "input_tag_id"
        })
    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区！")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            # "id": "input_area",
            "placeholder": "请输入地区！"
        }
    )
    length = StringField(
        label="片长",
        validators=[
            DataRequired("请输入片长！")
        ],
        description="片长",
        render_kw={
            "class": "form-control",
            # "id": "input_length",
            "placeholder": "请输入片长！"
        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("请选择上映时间！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "id": "input_release_time",
            "placeholder": "请选择上映时间！"
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 电影预告表单
class PreviewForm(FlaskForm):
    title = StringField(
        label="预告标题",
        validators=[
            DataRequired("请输入预告标题！")
        ],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入预告标题！"
        }
    )
    logo = FileField(
        label="预告封面",
        validators=[
            DataRequired("请上传预告封面")
        ],
        description="预告封面"
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 修改密码
class PwdForm(FlaskForm):
    oldpwd = StringField(
        label="预告标题",
        validators=[
            DataRequired("请输入预告标题！")
        ],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "id": "input_pwd",
            "placeholder": "请输入旧密码！"
        }
    )
    newpwd = StringField(
        label="预告标题",
        validators=[
            DataRequired("请输入预告标题！")
        ],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "id": "input_newpwd",
            "placeholder": "请输入新密码！"
        }
    )
    submit = SubmitField(
        "修改",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session.get("admin")
        admin = Admin.query.filter_by(adminname=name).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误")


# 权限表单
class AuthForm(FlaskForm):
    auth_name = StringField(
        label="权限名字",
        validators=[
            DataRequired("请输入权限标题！")
        ],
        description="权限名字",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入名字！"
        }
    )
    auth_add = StringField(
        label="权限地址",
        validators=[
            DataRequired("请输入地址！")
        ],
        description="权限地址",
        render_kw={
            "class": "form-control",
            "id": "input_url",
            "placeholder": "请输入权限地址！"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class": "btn btn-primary"
        }
    )


auth_list = Auth.query.all()


# 角色管理表单
class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired(u"请输入名称")
        ],
        description=u"角色名称",

        render_kw={
            "class": "form-control",
            "placeholder": "请输入角色名称！"
        }
    )
    auths = SelectMultipleField(
        label=u"权限列表",
        validators=[
            DataRequired(u"请输入地址")
        ],
        description=u"权限列表",
        coerce=int,
        choices=[(v.id, v.name) for v in auth_list],
        render_kw={
            "class": "form-control"
        }
    )
    submit = SubmitField(
        u"提交",
        render_kw={
            "class": "btn btn-primary"
        }
    )


role_list=Role.query.all()
class AdminAddForm(FlaskForm):
    adminname=StringField(
        label=u"管理员名称",
        validators=[
            DataRequired()
        ],
        description=u"管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称!"
        }
    )
    password = StringField(
        label=u"管理员密码",
        validators=[
            DataRequired()

        ],
        description=u"管理员密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员密码!"
        }
    )
    password2 = StringField(
        label=u"重复管理员密码",
        validators=[
            DataRequired(),
            #EqualTo(password,message="俩次密码不一致")
        ],
        description=u"管理员密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员密码!"
        }

    )

    role_id = SelectField(
        label=u"所属角色",
        validators=[
            DataRequired()
        ],
        description=u"所属角色",
        coerce=int,
        choices=[(v.id,v.name) for v in role_list],
        render_kw={
            "class": "form-control",
        }

    )
    submit=SubmitField(
        u"添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )