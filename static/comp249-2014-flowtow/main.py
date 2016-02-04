'''
Created on Mar 30, 2014

@author: Steve Cassidy
'''

from mock import list_images
from templating import render


def application(environ, start_response):
    """Main WSGI Application for FlowTow"""

    content = "<p>Hello World!</p>"
    mapping = {
               'title': 'Hello World',
               'content': content,}
    start_response("200 OK", [('content-type', 'text/html')])
    return render('index.html', mapping)
    
if __name__ == '__main__':
    
    from wsgiref import simple_server
    
    server = simple_server.make_server('localhost', 8000, application)
    print("listening on http://localhost:8000/ ...")
    server.serve_forever()
    
    