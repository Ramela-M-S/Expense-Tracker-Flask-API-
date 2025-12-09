from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired

class RegistrationForm(FlaskForm):
    username = StringField("UserName", validators=[DataRequired(), Length(min=3)])
    email = StringField("Email Id", validators = [DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message = "Password must match" )])
    submit = SubmitField("Sign Up")