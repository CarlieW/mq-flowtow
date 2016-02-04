'''
Created on Mar 4, 2014

@author: steve
'''

from wsgiref import simple_server
import os
from templating import render
from database import COMP249Db
import interface
import users
import login
from static import static_app, STATIC_URL_PREFIX
import comments
from images import default_app, myimages, upload

def about_app(environ, start_response):
    """generate the about page"""
    
    content = "<p>FlowTow is a new, exciting, photo sharing service like nothing you've seen before!</p>"
    mapping = {
               'title': 'About FlowTow',
               'content': content,}
               
    db = COMP249Db()
    user = users.user_from_cookie(db, environ)
    if user:
        mapping['user'] = user
        template = 'loggedin.html'
    else:
        template = 'index.html'
        
    start_response("200 OK", [('content-type', 'text/html')])
    return render(template, mapping)
    

def application(environ, start_response):
    """WSGI application to switch between different applications
    based on the request URI"""

    if environ['PATH_INFO'].startswith(STATIC_URL_PREFIX):
        return static_app(environ, start_response)
    
    elif environ['PATH_INFO'] == '/about':
        return about_app(environ, start_response)
        
    elif environ['PATH_INFO'] == '/my':
        return myimages(environ, start_response)
        
    elif environ['PATH_INFO'] == '/comment':
        return comments.application(environ, start_response)
        
    elif environ['PATH_INFO'] == '/login':
        return login.application(environ, start_response)
        
    elif environ['PATH_INFO'] == '/upload':
        return upload(environ, start_response)
    else:
        return default_app(environ, start_response)

from wsgiref.validate import validator

if __name__ == '__main__':
    server = simple_server.make_server('localhost', 8000, application)
    print("listening on http://localhost:8000/ ...")
    server.serve_forever()
    
    