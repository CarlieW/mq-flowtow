"""
 Main application for FlowTow image sharing app

 @Author: Steve.Cassidy@mq.edu.au

"""

import bottle
import os
import model
import users

app = bottle.Bottle()


@app.route('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename=filename, root='static')


@app.route('/about')
def about():
    """Generate the about page"""

    return bottle.template('about', title="About FlowTow!")


@app.route('/')
def index(db):
    """Generate the main page of the app"""

    info = {
        'user': users.session_user(db),
        'title': "¡Welcome to FlowTow!",
        'images': model.list_images(db, 3)
    }

    return bottle.template('index', info)


@app.route('/my')
def my(db):
    """Generate the view for an individual containing
    all of their images
    """

    user = users.session_user(db)

    if user is None:
        return bottle.redirect('/')

    info = {
        'user': user,
        'title': "¡Welcome to FlowTow!",
        'images': model.list_images(db, 3, user['nick'])
    }

    return bottle.template('index', info)


@app.post('/like')
def like(db):
    """Add a like to an existing image"""

    filename = bottle.request.forms.get('filename')

    user = users.session_user(db)
    if user is not None:
        nick = user['nick']
    else:
        nick = None
    model.add_like(db, filename, nick)

    bottle.redirect('/')


@app.post('/login')
def login(db):
    """Process a login request"""

    nick = bottle.request.forms.get('nick')
    password = bottle.request.forms.get('password')

    if users.login(db, nick, password):
        bottle.redirect('/')
    else:
        return bottle.template('general', title='Login Error', content='Login Failed, please try again')


@app.post('/logout')
def logout():
    """Process a logout request"""

    users.logout()
    bottle.redirect('/')


@app.post('/upload')
def upload(db):
    """Process a file upload request"""

    user = users.session_user(db)
    if user is None:
        # not allowed to upload, redirect to home
        return bottle.redirect('/')

    imagefile = bottle.request.files.get('imagefile')

    if imagefile is not None:
        imagefile.save(os.path.join(os.path.dirname(__file__), 'static', 'images'), overwrite=True)

        model.add_image(db, imagefile.filename, user['nick'])

    return bottle.redirect('/my')


if __name__ == '__main__':

    from bottle.ext import sqlite, beaker
    from database import DATABASE_NAME

    # bottle debug mode
    bottle.debug()

    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))

    # install the session middleware
    session_opts = {
        'session.type': 'memory',
    }
    beaker_app = beaker.middleware.SessionMiddleware(app, session_opts)

    bottle.run(app=beaker_app, debug=True, port=8010)


