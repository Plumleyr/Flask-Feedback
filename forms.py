from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email

class RegisterForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])

    password = PasswordField("Password", validators = [InputRequired()])

    email = StringField("Email", validators = [InputRequired(), Email()])

    firstname = StringField("First Name", validators = [InputRequired()])

    lastname = StringField("Last name", validators = [InputRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])

    password = PasswordField("Password", validators = [InputRequired()])

class FeedbackForm(FlaskForm):

    title = StringField("Title", validators = [InputRequired()])

    content = TextAreaField("Content", validators = [InputRequired()])
