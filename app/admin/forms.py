from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BTCCodeForm(FlaskForm):
    host = StringField(
        'URL of BTCPay Instance (include the "https://")',
        validators=[DataRequired()]
    )
    code = StringField('Pairing Code', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SupportLevelForm(FlaskForm):
    # TODO
