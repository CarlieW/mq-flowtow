''' Handling of comments '''

from database import COMP249Db
import interface
import cgi


def application(environ, start_response):
    """App to respond to add comment form submission"""

    form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

    if 'comment' in form:
        comment = form.getvalue('comment')
        image = form.getvalue('image')

        db = COMP249Db()
        usernick = 'bob' # should be current logged in user
        interface.add_comment(db, image, comment, usernick)


    # respond with a redirect to the home page
    headers = [('location', '/')]
    start_response('303 See Other', headers)
    return [b'redirect']
