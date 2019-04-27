"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app,db
from app.models import Follow,Users,Likes
from flask import render_template, request,jsonify
from .forms import RegistrationForm,LoginForm
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash,check_password_hash
import os
import datetime
import jwt
from functools import wraps
###
# Routing for your application.
###


# Please create all new routes and view functions above this route.
# This route is now our catch all route for our VueJS single page
# application.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    Because we use HTML5 history mode in vue-router we need to configure our
    web server to redirect all routes to index.html. Hence the additional route
    "/<path:path".
    Also we will render the initial webpage and then let VueJS take control.
    """
    return render_template('index.html')
    
    
@app.route('/api/users/register',methods=["POST"])
def register():
    form = RegistrationForm()
    if request.method=='POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        location=form.location.data
        biography=form.biography.data
        lastname=form.lastname.data
        firstname=form.firstname.data
        email=form.email.data
        photo = form.photo.data
        date = str(datetime.date.today())
        filename = username+secure_filename(photo.filename)
        user = Users(username=username, password=password, first_name=firstname, last_name=lastname, email=email, location=location, biography=biography, profile_photo=filename, joined_on=date)
        photo.save(os.path.join(app.config['PROFILE_IMAGES'], filename))
        db.session.add(user)
        db.session.commit()
            
        return jsonify(message = "User successfully registered")

    
    return jsonify(errors=form_errors(form))

@app.route('/api/auth/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = Users.query.filter_by(username=username).first()
        if user is not None or check_password_hash(user.password, password):
            
            payload = {'user': user.username}
            jwt_token = jwt.encode(payload,'secret',algorithm = "HS256")
            response = {'message': 'User successfully logged in','token':jwt_token, "user_id": user.id}
            
            return jsonify(response)
            
        return jsonify(errors=["Username or password is incorrect"])
    
    return jsonify(errors=form_errors(form))

@app.route('/api/users/<user_id>/posts', methods =['GET','POST'])
def post(user_id):
    if request.method == 'GET':
        posts = Post.query.filter_by(id = user_id).all()
        user = UserProfile.query.filter_by(id = user_id).first()
        followers = len(Follows.query.filter_by(id=user_id).all())
        response = {"postinfo": { "firstname": user.first_name, "lastname": user.last_name, "location" :user.location, "datejoined": user.date_joined,"biography": user.biography,"profilepic":os.path.join(app.config['PROFILE_PICT'], user.photograph ),"tposts": len(posts),"followers": followers, "images": []}}
        for i in posts:
            spost = {"id": i.post_id, "uid": i.user_id, "photo": os.path.join(app.config['UPLOAD_FOLDER'], i.photo) , "caption": i.caption, "pcreation": i.created_on}
            response["postinfo"]["images"].append(spost)
        return jsonify(response)
    
    if request.method == 'POST':
        filefolder = app.config['UPLOAD_FOLDER']
        form = PostsForm()
        if form.validate_on_submit():
            uid = form.user_id.data
            image = request.files['image']
            caption = form.caption.data
            user = UserProfile.query.filter_by(id=uid).first()
            filename = secure_filename(image.filename)
            creation = datetime.date.today().strftime('%Y-%m-%d')
            post = Post(id=uid,photo=filename,caption=caption ,created_on=creation)
            image.save(os.path.join(filefolder, filename))
            db.session.add(post)
            db.session.commit()
            return jsonify(message= "Post successfully created ")
        return jsonify(errors=form_errors(form))
        
@app.route('/api/users/<user_id>/follow', methods = ['POST'])
def follow(user_id):
    requests = request.get_json()
    hold = requests['user_id']
    holdx = requests['follower_id']
    testfollowing = Follows.query.filter_by(follower_id=holdx).all()
    if testfollowing is not None:
        for f in testfollowing:
            if f.user_id == hold:
                return jsonify(message="Already Following")
    
    follow = Follows(follower_id = requests['follower_id'], user_id = requests['user_id'])
    db.session.add(follow)
    db.session.commit()
    return jsonify(message="Follow Successful")
    
# Here we define a function to collect form errors from Flask-WTF
# which we can later use
@app.route('/api/posts', methods = ['GET'])
def AllPosts():
    Posts = Post.query.all()
    tpost = []
    for i in Posts:
        user = UserProfile.query.filter_by(id=i.user_id).first()
        likes = len(Likes.query.filter_by(post_id=i.post_id).all())
        spost = {"id": i.post_id, "uid": i.user_id, "username": user.username, "profile_pic": os.path.join(app.config['UPLOAD_FOLDER'], user.photograph), "pic":os.path.join(app.config['PROFILE_IMAGES'], i.photo ), "caption": i.caption, "pcreation": i.created_on, "likes" : likes}
        tpost.append(spost)
    return jsonify(posts=tpost)
        
@app.route('/api/posts/<post_id>/like',methods = ['POST'])
def like(post_id):
    requests= request.get_json()
    post_id = requests["post_id"]
    user_id = requests["user_id"]
    postx = Post.query.filter_by(post_id=post_id).first()
    likesx = Likes.query.filter_by(post_id=post_id).all()
    if likesx is not None:
        for like in likesx:
            if like.id == user_id:
                return jsonify(message="Post has been liked already.")
    added = Likes(id = user_id,post_id = post_id)
    db.session.add(added)
    db.session.commit()
    tlikes = len(Likes.query.filter_by(post_id=post_id).all())
    return jsonify({"message": 'Post liked', "likes":tlikes })
    
    
@app.route('/api/auth/logout', methods = ['GET'])
def logout():
    return jsonify(message= "User successfully logged out.")
    
    
    
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


          



###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")