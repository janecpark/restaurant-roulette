from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional
from models import db, User, Restaurant, Favorite


class UserForm(FlaskForm):
    """For for adding new user"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])
    email = StringField('E-mail', validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Form for logging in"""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

