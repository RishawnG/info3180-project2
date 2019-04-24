"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app
from flask import render_template, request,jsonify
from .forms import UploadForm
from werkzeug.utils import secure_filename
import os
import datetime
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
        photo.save(os.path.join("./app",app.config['PROFILE_IMAGES'], filename))
        db.session.add(user)
        db.session.commit()
        return jsonify(message = "User successfully registered")
    return jsonify(errors=form_errors(form))


@app.route('/api/auth/login',methods=['POST'])
def login():
    form =LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user=Users.query.filter_by(username=username).first()
        if user!= None and password=password:
        
    
@app.route('/api/auth/logout', methods = ['GET'])
# @token_authenticate
def logout():
    return jsonify(message= "User successfully logged out.")
        
        
        
        
        
        
        
# Here we define a function to collect form errors from Flask-WTF
# which we can later use
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