
import os

STATIC_URL_PREFIX = "/static"
STATIC_FILE_DIR = os.path.join(os.path.dirname(__file__), 'static')
    
MIME_TABLE = {'.txt': 'text/plain',
              '.html': 'text/html',
              '.css': 'text/css',
              '.jpg': 'image/jpeg',
              '.js': 'application/javascript',
             }            
    
def content_type(path):
    """Return a guess at the mime type for this path
    based on the file extension"""
    
    name, ext = os.path.splitext(path)
    
    if ext in MIME_TABLE:
        return MIME_TABLE[ext]
    else:
        return "application/octet-stream"    
    
def static_app(environ, start_response):
    """Serve static files from the directory named
    in STATIC_FILES"""
    
    path = environ['PATH_INFO']
    # we want to remove '/static' from the start
    path = path.replace(STATIC_URL_PREFIX, STATIC_FILE_DIR)
    
    if os.path.exists(path):
        h = open(path, 'rb')
        content = h.read()
        h.close()
        
        headers = [('content-type', content_type(path))]
        start_response('200 OK', headers)
        return [content]
    else:
        return show_404_app(environ, start_response)
        
        

def show_404_app(environ, start_response):
    """Return a 404 not found response"""
    
    
    mapping = {'content': '<p>That page is unknown. Return to the <a href="/">home page</a></p>',
               'title': 'Page Not Found',
               }
    headers = [('content-type', 'text/html')]
    start_response('404 Not Found', headers)
    return render('index.html', mapping) 
    
    