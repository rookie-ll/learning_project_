from wtforms import StringField, IntegerField, Form
from wtforms.validators import DataRequired, Length, NumberRange


class SearchFrom(Form):
    q = StringField(
        validators=[
            DataRequired(),
            Length(min=1, max=30, message="请输入1-30个字符")
        ]
    )
    page = IntegerField(
        validators=[
            DataRequired(),
            NumberRange(min=1, max=99, message="你特么干第几页去了？")
        ],
        default=1
    )
