from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sucika.models import User


class ViewBySID(FlaskForm):
    sid = StringField('SID', validators=[DataRequired()])
    submit = SubmitField('Click Me!')


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class Register(FlaskForm):
    fullname = StringField('Full Name', validators=[
                           DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[
                                    DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Account')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email is already taken!')


class Upload(FlaskForm):
    file = FileField('file')
    submit = SubmitField('Upload')
