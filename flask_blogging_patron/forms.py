from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField,\
       RadioField
from wtforms.validators import DataRequired


class BlogEditor(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    text = TextAreaField("text", validators=[DataRequired()])
    tags = RadioField(
        'Optional Parameters',
        choices=[
            ('normal', 'Post this as a subscriber update and email to all subscribers.'),
            ('noemail', 'Post this as a subscriber update, but do not email it.'),
            ('public', 'Post this to the public homepage rather than updates.'),
        ]
    )
    draft = BooleanField("draft", default=False)
    submit = SubmitField("submit")
