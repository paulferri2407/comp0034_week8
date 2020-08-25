from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from my_app.models import User


class SignupForm(FlaskForm):
    first_name = StringField(label='First name', validators=[DataRequired(message='First name required')])
    last_name = StringField(label='Last name', validators=[DataRequired(message='Last name required')])
    email = EmailField(label='Email address', validators=[DataRequired(message='Email adddress required')])
    password = PasswordField(label='Password', validators=[DataRequired(message='Password required')])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')


class LoginForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
