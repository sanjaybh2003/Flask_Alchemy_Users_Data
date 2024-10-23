from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)], render_kw={"placeholder": "Enter your username"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)], render_kw={"placeholder": "Enter your password"})
    submit = SubmitField('Login')

class CreateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)], render_kw={"placeholder": "Enter your username"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)], render_kw={"placeholder": "Enter your password"})
    about_user = TextAreaField('About User', validators=[Optional()], render_kw={"placeholder": "Tell us about yourself"})
    submit = SubmitField('Create User')

class DeleteUserForm(FlaskForm):
    hidden_tag = HiddenField()