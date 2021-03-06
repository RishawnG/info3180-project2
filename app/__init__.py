from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)


csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = 'v\xf9\xf7\x11\x13\x18\xfaMYp\xed_\xe8\xc9w\x06\x8e\xf0f\xd2\xba\xfd\x8c\xda'

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://project1user:project1password@localhost/project2" 
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://peqfkcaqcmmvvy:1b798ef612197d0df7153e6a96c5e100209ab89bbb897e2544846d951c1f8cd4@ec2-54-197-234-117.compute-1.amazonaws.com:5432/dfd4sioerg43nm'"

UPLOAD_FOLDER = './app/static/uploads/'
Profile_Images= './app/static/profilepics'
server_image='./app/static/serverimage'

app.config['PROFILE_IMAGES']=Profile_Images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SERVER_IMAGE']=server_image

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

app.config.from_object(__name__)

from app import views

