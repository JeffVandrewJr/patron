from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, \
        PasswordField
from wtforms.validators import DataRequired


class BTCCodeForm(FlaskForm):
    host = StringField(
        'URL of BTCPay Instance (include the "https://")',
        validators=[DataRequired()]
    )
    code = StringField('Pairing Code', validators=[DataRequired()])
    submit = SubmitField('Submit')


class GAForm(FlaskForm):
    code = StringField(
        'Enter Tracking Code (begins with "UA")',
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')


class IssoForm(FlaskForm):
    code = StringField(
        'Enter a comment moderation password:',
        validators=[DataRequired()]
    )
    submit = SubmitField('Activate User Comments')


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


class EmailSetupForm(FlaskForm):
    outgoing_email = StringField(
        'Enter the email to show on outbound emails:',
        validators=[DataRequired()]
    )
    server = StringField(
        'Enter Email Host Name',
        validators=[DataRequired()]
    )
    port = IntegerField(
        'Enter Server Port (normally 587)',
        validators=[DataRequired()]
    )
    username = StringField(
        'Enter email username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Enter email password',
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')
