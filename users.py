'''
Created on Mar 26, 2012

@author: steve
'''

import bottle

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'

def check_login(db, usernick, password):
    """returns True if password matches stored"""

    cursor = db.cursor()
    # get the user details
    cursor.execute('select password from users where nick=?', (usernick,))
    row = cursor.fetchone()
    if row:
        # check that password matches
        storedpw = row[0]
        return storedpw == db.crypt(password)
    else:
        return False


def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """

    # test to see whether we have one already
    cursor = db.cursor()
    # first check that this is a valid user
    cursor.execute('select nick from users where nick=?', (usernick,))
    row = cursor.fetchone()
    if not row:
        # unknown user
        return None

    usernick = row[0]

    cursor.execute('select sessionid from sessions where usernick=?', (usernick,))
    row = cursor.fetchone()
    if row:
        sessionid = row[0]
    else:
        sessionid = db.crypt(usernick)
        # insert a new row into session table
        cursor.execute('insert into sessions (sessionid, usernick) values (?, ?)', (sessionid, usernick))
        db.commit()

    # set the cookie in the response
    bottle.response.set_cookie(COOKIE_NAME, sessionid)

    return sessionid


def delete_session(db, usernick):
    """remove all session table entries for this user"""

    cursor = db.cursor()
    cursor.execute("delete from sessions where usernick=?", (usernick,))
    db.commit()


def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""

    sessionid = bottle.request.get_cookie(COOKIE_NAME)

    # look in the sessions table
    cursor = db.cursor()
    cursor.execute("select usernick from sessions where sessionid=?", (sessionid,))

    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        # we didn't find the session, so we can't say who this is
        return None
