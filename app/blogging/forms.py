from flask_blogging.forms import BlogEditor
from wtforms import StringField, TextAreaField, SubmitField, BooleanField,\
        SelectField
from wtforms.validators import DataRequired


class ModifiedBlogEditor(BlogEditor):
    title = StringField("title", validators=[DataRequired()])
    text = TextAreaField("text", validators=[DataRequired()])
    tags = SelectField(
        'Optional Parameters',
        choices=[
            ('noemail', 'Do Not Email this Update')
            ('public', 'Post this to homepage rather than updates.')
        ]
    )
    draft = BooleanField("draft", default=False)
    submit = SubmitField("submit")
