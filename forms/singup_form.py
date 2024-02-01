from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email


class SingUpForm(FlaskForm):
    email = StringField("Email", validators=[Email(), DataRequired()])
    username = StringField("User name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    repeat = PasswordField("RepeatPassword", validators=[DataRequired()])
    submit = SubmitField("Submit")