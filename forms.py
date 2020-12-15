from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class ViewBySID(FlaskForm):
    sid = StringField('SID', validators=[DataRequired()])
    submit = SubmitField('Click Me!')