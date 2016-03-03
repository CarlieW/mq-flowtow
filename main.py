'''
Created on Mar 4, 2014

@author: steve
'''

from bottle import Bottle, template, static_file, request, response, HTTPError, debug
import interface
import users
from database import COMP249Db

# for deployment we need to make sure we're in the right directory
#import os
#os.chdir(os.path.dirname(__file__))

COOKIE_NAME = 'sessionid'

application = Bottle()
debug()

@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


@application.route('/about')
def about():
    """generate the about page"""

    return template('about', title="About FlowTow")

@application.route('/')
def index():

    db = COMP249Db()

    info = {}

    info['user'] = users.session_user(db)
    info['title'] = "¡Welcome to FlowTow!"

    info['images'] = interface.list_images(db, 3)

    return template('index', info)

@application.route('/my')
def my():

    db = COMP249Db()

    info = {}

    info['user'] = users.session_user(db)

    if info['user'] == None:
        # redirect to the home page
        response.status = 303
        response.set_header('Location', '/')
        return "Redirect"


    info['title'] = "¡Welcome to FlowTow!"

    info['images'] = interface.list_images(db, 3, info['user'])

    return template('index', info)


@application.post('/like')
def like():
    """Add a like to an existing image"""

    filename = request.forms.get('filename')

    db = COMP249Db()
    usernick = users.session_user(db)
    interface.add_like(db, filename, usernick)


    # respond with a redirect to the home page
    response.status = 303
    response.set_header('Location', '/')
    return "Redirect"


@application.post('/login')
def login():
    """Process a login request"""

    db = COMP249Db()

    nick = request.forms.get('nick')
    password = request.forms.get('password')

    if users.check_login(db, nick, password):

        users.generate_session(db, nick)

        response.status = 303
        response.set_header('Location', '/')
        return "Redirect"
    else:
        return template('general', title='Login Error', content='Login Failed, please try again')

@application.post('/logout')
def logout():
    """Process a logout request"""

    db = COMP249Db()

    usernick = users.session_user(db)
    users.delete_session(db, usernick)

    response.status = 303
    response.set_header('Location', '/')
    return "Redirect"



@application.post('/upload')
def upload():

    db = COMP249Db()

    usernick = users.session_user(db)
    if usernick == None:
        # not allowed to upload, redirect to home
        response.status = 303
        response.set_header('Location', '/')
        return "Redirect"

    imagefile = request.files.get('imagefile')

    if imagefile is not None:
        imagefile.save('static/images', overwrite=True)

        interface.add_image(db, imagefile.filename, usernick)

    response.status = 303
    response.set_header('Location', '/my')
    return "Redirect"



if __name__ == '__main__':
    debug()
    application.run()
