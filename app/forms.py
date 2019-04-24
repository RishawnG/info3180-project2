from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, EmailField
from wtforms.validators import InputRequired


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    firstname=StringField("Firstname",validators=[InputRequired("Enter your firstname")])
    lastname=StringField("Lastname",validators=[InputRequired("Enter your lastname")])
    email=EmailField("Email",validators=[InputRequired("Please enter a valid email address")])
    location = StringField("Location", validators=[InputRequired("Enter your location")])
    biography = TextAreaField("Biography", validators =[InputRequired("Say Something about Yourself")])
    photo=FileField("Profile Picture",validators=[FileRequired("Upload your profile picture here"),FileAllowed(['jpg','png'],'')])
    

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators =[InputRequired()] )

class PostsForms(FlaskForm):
    photo= FileField("Post Pics",validators=[FileRequired("Upload your profile picture here"),FileAllowed(['jpg','png'],'')])
    caption = TextAreaField("Caption" validators =[InputRequired("Say Something")]) 
