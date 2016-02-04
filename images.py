"""Application generating image list pages
 - home page
 - my images
 
"""
from wsgiref import simple_server
import os
import cgi

from templating import render
from database import COMP249Db
import interface
import users

UPLOAD_FORM = """
    <form id='uploadform' method='post' action='/upload' enctype="multipart/form-data">
    <fieldset class='form-group'>
      <legend>Upload New Image</legend>
       <input class='form-control' type='file' name='file'>
       <input type='hidden' name='user' value='%s'>
       <input class='btn btn-primary' type='submit' value="Upload File">
      </fieldset>
    </form>
"""


COMMENT_FORM = """
<form role='form' method='post' action='/comment'>
  <div class='form-group'>
  <input type='hidden' name='image' value='%s'>
  <input class='form-control' type='text' name='comment' placeholder='Enter your comment here'>
  <input class='btn btn-primary' type='submit' value='Submit'>
  </div>
</form>"""

def encode_string(text):
    """Replace any markup in the text with HTML escape characters"""
    
    
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    
    return text


def format_image(db, img_tuple):
    """Given an image tuple with (path, date, owner) 
    return a string with suitable HTML to display the image"""
    
    tpl = """<div class='flowtow'>
    <p><span class='date'>%s</span> <span class='name'>%s</span></p>
    <img src='/static/images/%s'>
    """
    
    page = tpl % (img_tuple[1], img_tuple[2], img_tuple[0])
    
    page += "<ul>"
    for comment in interface.list_comments(db, img_tuple[0]):
        page += "<li>" + encode_string(comment) + "</li>"
    page += "</ul>"
    
    page += COMMENT_FORM % img_tuple[0]
    
    page += "</div>"
    
    return page
    


def default_app(environ, start_response):
    
    headers = [('content-type', 'text/html')]
    start_response('200 OK', headers)
    
    db = COMP249Db()
    
    content = ""
    for image in interface.list_images(db, 3):
        content += format_image(db, image)
    
    mapping = {
               'title': 'Welcome to FlowTow',
               'content': content,}
    
    user = users.user_from_cookie(db, environ)
    if user:
        mapping['user'] = user
        template = 'loggedin.html'
    else:
        template = 'index.html'
    
    return render(template, mapping)



def myimages(environ, start_response):
    
    headers = [('content-type', 'text/html')]
    db = COMP249Db()
    
    user = users.user_from_cookie(db, environ)
    if user:
  
        content = UPLOAD_FORM % user
        
        for image in interface.list_images_for_user(db, user):
            content += format_image(db, image)
    
        mapping = {'title': 'Welcome to FlowTow',
                   'user': user,
                   'content': content,}

        start_response('200 OK', headers)
        return render('loggedin.html', mapping)
    else:
        # not allowed to see this page
        # redirect to home
        
        headers = [('content-type', 'text/html'),
                   ('Location', '/')]
                   
        start_response('303 See Other', headers)
        return render('index.html', {})
        
import random

def upload(environ, start_response):
    """Application to handle file upload"""
    
    formdata = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
    db = COMP249Db()
    
    user = users.user_from_cookie(db, environ)
    if user:
        # get the file field
        if 'file' in formdata and formdata['file'].filename != '':
            
            file_data = formdata['file'].file.read()
        
            # write out to a new file in the image directory
            # we need a unique filename
            imgname = str(int(random.random()*1000000)) + "-" + formdata['file'].filename
            target = os.path.join(os.path.dirname(__file__), 'static', 'images', imgname)
    
            f = open(target, 'wb')
            f.write(file_data)
            f.close()
        
            # add the new image to the database
            interface.add_image(db, imgname, user)
        else:
            print("no file field")
        
        # response is a redirect to My Images
        headers = [('content-type', 'text/html'),
                   ('Location', '/my')]
               
        start_response('303 See Other', headers)
        return render('index.html', {})
    else:
        # no user so return a forbidden response
        
        headers = [('content-type', 'text/html')]
        
        mapping = {'title': 'Forbidden',
                    'content': "<p>You need to be logged in to upload an image.</p>"
                }
        start_response('403 Forbidden', headers)
        return render('index.html', mapping)
        
        
