"""
Login and logout implemented using beaker sessions

Author: Steve.Cassidy@mq.edu.au
"""

import bottle
import database


def login(db, usernick, password):
    """returns True if password matches stored"""

    session = bottle.request.environ.get('beaker.session')

    cursor = db.cursor()
    # get the user details
    cursor.execute('select password from users where nick=?', (usernick,))
    row = cursor.fetchone()
    if row:
        # check that password matches
        if row['password'] == database.encode(password):
            session['user_id'] = usernick
            session.save()
            return True

    return False


def logout():
    """remove all session table entries for this user"""

    session = bottle.request.environ.get('beaker.session')
    session.delete()


def session_user(db):
    """try to
    retrieve the user from the sessions table
    return a tuple (usernick, avatar) or None if no valid session is present"""

    session = bottle.request.environ.get('beaker.session')
    if 'user_id' in session:

        cursor = db.cursor()
        # get the user details
        cursor.execute('select nick, avatar from users where nick=?', (session['user_id'],))

        row = cursor.fetchone()
        if row:
            return row

    # return None if we didn't find anything
    return None

