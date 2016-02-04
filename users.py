'''
Created on Mar 26, 2012

@author: steve
'''

from http.cookies import SimpleCookie

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'

def check_login(db, useremail, password):
    """returns True if password matches stored"""

    cursor = db.cursor()
    # get the user details
    cursor.execute('select password from users where email=?', (useremail,))
    row = cursor.fetchone()
    if row:
        # check that password matches
        storedpw = row[0]
        return storedpw == db.crypt(password)
    else:
        return False


def generate_session(db, useremail):
    """create a new session, return a cookie obj with session key
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, the cookie should use the existing
    sessionid
    """

    # test to see whether we have one already
    cursor = db.cursor()
    # first check that this is a valid user
    cursor.execute('select email from users where email=?', (useremail,))
    if not cursor.fetchall():
        # unknown user
        return None

    cursor.execute('select sessionid from sessions where useremail=?', (useremail,))
    row = cursor.fetchone()
    if row:
        sessionid = row[0]
    else:
        sessionid = db.crypt(useremail)
        # insert a new row into session table
        cursor.execute('insert into sessions (sessionid, useremail) values (?, ?)', (sessionid, useremail))
        db.commit()

    # make the cookie to return
    cookie = SimpleCookie()
    cookie[COOKIE_NAME] = sessionid

    return cookie


def delete_session(db, useremail):
    """remove all session table entries for this user"""

    cursor = db.cursor()
    cursor.execute("delete from sessions where useremail=?", (useremail,))
    db.commit()


def user_from_cookie(db, environ):
    """check whether HTTP_COOKIE set, if it is,
    and if our cookie is present, try to
    retrieve the user email from the sessions table
    return useremail or None if no valid session is present"""

    if 'HTTP_COOKIE' in environ:
        cookie = SimpleCookie(environ['HTTP_COOKIE'])
        if COOKIE_NAME in cookie:
            sessionid = cookie[COOKIE_NAME].value
            # look in the sessions table
            cursor = db.cursor()
            cursor.execute("select useremail from sessions where sessionid=?", (sessionid,))

            row = cursor.fetchone()
            if row:
                return row[0]

    # we didn't find the session, so we can't say who this is
    return None

