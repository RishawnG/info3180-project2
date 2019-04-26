from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import TextAreaField,StringField,PasswordField
from wtforms.validators import InputRequired
from werkzeug import secure_filename


class RegistrationForm(FlaskForm):
    username=StringField("Username",validators=[InputRequired("Enter your Username")])
    password=PasswordField("Password",validators=[InputRequired("Enter your Password")])
    location=StringField("Location",validators=[InputRequired("Enter your Location")])
    biography=TextAreaField("Biography",validators=[InputRequired(" Please type a biography")])
    firstname=StringField("Firstname",validators=[InputRequired("Enter your firstname")])
    lastname=StringField("Lastname",validators=[InputRequired("Enter your lastname")])
    email=StringField("Email",validators=[InputRequired("Please enter a valid email address")])
    photo=FileField("Profile Picture",validators=[FileRequired("Upload your profile picture here"),FileAllowed(['jpg','png'],'')])
    
class LoginForm(FlaskForm):
    username=StringField("Username",validators=[InputRequired("Enter your Username")])
    password=PasswordField("Password",validators=[InputRequired("Enter your Password")])