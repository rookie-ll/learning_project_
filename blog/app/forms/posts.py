from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Length, DataRequired, ValidationError
from app.models import Category


# 发表博客的表单类
class SendPosts(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories.choices = [(v.id, v.name) for v in Category.query.all()]

    title = StringField(
        '标题',
        validators=[
            DataRequired('标题内容不能为空'),
            Length(min=3, max=20, message='标题内容在3~20字之间')
        ],
        render_kw={"placeholder": '请输入标题'}
    )
    article = TextAreaField(
        '博客内容'
        , validators=[
            DataRequired('博客内容不能为空'),
            Length(min=20, max=2000, message='博客内容在20~1000字之间')
        ],
        render_kw={"placeholder": '请输入博客内容'}
    )
    categories = SelectField(
        "标签列表",
        validators=[
            DataRequired(u"请选择一个标签")
        ],
        description=u"标签列表列表",
        coerce=int,
        choices="",
        render_kw={
            "class": "form-control"
        }
    )
    submit = SubmitField('发表')


# 发表评论和回复的表单类
class Comment(FlaskForm):
    content = TextAreaField(
        '评论内容',
        validators=[
            DataRequired('内容不能为空'),
            Length(min=5, max=100, message='博客内容在5~100字之间')
        ]
    )
    submit = SubmitField('发表')
