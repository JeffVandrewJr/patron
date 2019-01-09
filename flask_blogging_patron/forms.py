from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField,\
       RadioField, HiddenField
from wtforms.validators import DataRequired


class BlogEditor(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    text = TextAreaField("text")
    tags = RadioField(
        'Optional Parameters',
        choices=[
            ('NORMAL', 'Post this as a subscriber update and email to all subscribers.'),
            ('NOEMAIL', 'Post this as a subscriber update, but do not email it.'),
        ]
    )
    draft = BooleanField("draft", default=False)
    submit = SubmitField("submit")


class HomePageEditor(BlogEditor):
    tags = HiddenField(default='PUBLIC')
