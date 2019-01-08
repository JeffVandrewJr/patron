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


class SquareSetupForm(FlaskForm):
    application_id = StringField(
        'Square Application ID',
        validators=[DataRequired()]
    )
    location_id = StringField(
        'Square Location ID',
        validators=[DataRequired()]
    )
    access_token = StringField(
        'Square Access Token',
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')
