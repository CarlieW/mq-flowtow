
from wsgiref import simple_server
import database, users, templating
import cgi


def application(environ, start_response):
    """A WSGI application to handle login and logout 
    """
    
    formdata = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
    db = database.COMP249Db()
    response_code = "200 OK"
    headers = [('content-type', 'text/html')]
    
    if 'email' in formdata and "password" in formdata:
        email = formdata.getvalue('email')
        password = formdata.getvalue('password')
        if users.check_login(db, email, password):
            cookie = users.generate_session(db, email) 
            message = "Login successful."
            # response after successful login is a redirect to the home page
            response_code = '303 See Other'
            headers = [('content-type', 'text/html'),
                       ('Set-Cookie', cookie[users.COOKIE_NAME].OutputString()),
                       ('Location', '/')]
        else:
            message = "Login Failed, please try again."
            
    elif 'logout' in formdata:
        user = users.user_from_cookie(db, environ)
        users.delete_session(db, user)
        message = "Logged out"
        response_code = '303 See Other'
        headers = [('content-type', 'text/html'),
                   ('Location', '/')]        
    else:
        message = "Unknown action"
        
    content = {'title': "Login problem", 'content': message}
    
    start_response(response_code, headers)
    return templating.render("index.html", content)