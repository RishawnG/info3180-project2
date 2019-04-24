from . import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255), default= "Something")
    first_name = db.Column(db.String(80), default= "Something")
    last_name = db.Column(db.String(80), default= "Something")
    email= db.Column(db.String(20), default= "Something")
    location= db.Column(db.String(60), default= "Something")
    biography= db.Column(db.Text,nullable = False, default= "Something")
    profile_photo= db.Column(db.String(20), default= "Something")
    joined_on = db.Column(db.String(20), default= "Something")
    post = db.relationship("Post", backref= "author", lazy =True)
    like = db.relationship("Likes", backref = "liker")
    


    def __init__(self,first_name,last_name,username):
        self.first_name=first_name
        self.last_name=last_name
        self.username=username
        


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)

class Post(db.Model):
    id= db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    photo = db.Column(db.String )
    caption = db.Column(db.Text)
    created_on = db.Column(db.String(20))
    likes = db.relationship('Likes',backref="Likers")

class Likes(db.Model):
    id= db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))

##class Follows(db.Model):
  #####follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
