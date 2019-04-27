from . import db
from werkzeug.security import generate_password_hash


class Users(db.Model):
    
    __tablename__ = 'userprofile'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255),nullable = False )
    first_name = db.Column(db.String(255),)
    last_name = db.Column(db.String(255),)
    email= db.Column(db.String(200), default= "Something")
    location= db.Column(db.String(255), default= "Something")
    biography= db.Column(db.Text,nullable = False, default= "Something")
    profile_photo= db.Column(db.String(200), default= "default.png")
    joined_on = db.Column(db.String(200), default= "Something")
    post = db.relationship("Post", backref= "author", lazy =True)
    like = db.relationship("Likes", backref = "liker")
    follower = db.relationship("Follow",foreign_keys="Follow.user_id")#, backref= "followeee")
    followee = db.relationship("Follow", foreign_keys="Follow.follower_id")#, backref = "followeee")
   

    def __init__(self, username, password, first_name, last_name, email, location, biography, profile_photo, joined_on):
        self.username = username
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = profile_photo
        self.joined_on = joined_on
        


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
    user_id = db.Column(db.Integer,db.ForeignKey('userprofile.id'))
    photo = db.Column(db.String )
    caption = db.Column(db.Text)
    created_on = db.Column(db.String(20))
    likes = db.relationship('Likes',backref="Likers")

    def __init__(self,user_id,photo,caption,created_on):
        self.user_id = user_id
        self.photo = photo
        self.caption = caption
        self.created_on = created_on
    
class Likes(db.Model):
    id= db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('userprofile.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))

    def __init__(self,post_id,user_id):
        self.user_id = user_id
        self.post_id = post_id



class Follow(db.Model):
    id= db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('userprofile.id'))
    follower_id = db.Column(db.Integer, db.ForeignKey('userprofile.id'))

    def __init__(self,user_id,follower_id):
        self.user_id= user_id
        self.follower_id = follower_id
        