FlowTow Project Functional Requirements
=======================================

Brief
-----

FlowTow is a new, exciting, photo sharing service like nothing you've seen before! 
It allows users to upload photos to share with friends who can like or comment on
them. 

Requirements
------------

Functional Tests

As a visitor to the site, when I load the home page I see a banner with "Welcome to FlowTow". 

As a visitor to the site, when I load the home page I see three images displayed, each
labelled with a date, a user name and the comments on the image.

	Each image will be contained in a <div> with class 'flowtow', that div will
	contain the date, username and comments.


As a visitor to the site, when I load the home page I see a comment form below each
image with the placeholder text "Enter your comment here" and a button labelled "Submit"

As a visitor to the site, when I load the home page I see a link to another page
called "About this site".

As a visitor to the site, when I click on the link "About this site" I am taken to 
a page that contains the site manifesto, including the words "FlowTow is a new, exciting, 
photo sharing service like nothing you've seen before!"

As a visitor to the site, I notice that all the pages on the site have the same
design with the same colours and fonts used throughout. 

Unit Tests

There is a procedure 'list_images' that takes a single argument 'n' and returns a list of 
the most recent 'n' images that have been uploaded along with their details.  The return
value will be a list of tuples with one tuple per image, each tuple will contain four
elements: (path, date, owner, comments).  'path' is the path to the image relative to 
the default image directory, 'date' is a date string, 'owner' is the id of the owner
of the image and 'comments' is a list of comment strings for this image.

	Note that in the first round of implementation we will use a 'mock' version of
	this procedure that always returns the same result.



Level 2
-------

Functional Tests

As for level one plus:

As a visitor to the site, when I enter a comment into the text box below an image and press
the "Submit" button, the page returned has the text of my comment below the same
image along with the time it was posted.

Unit Tests

This level adds an SQLITE database to the implementation.  

There is a procedure 'list_comments' that takes a single argument that is the 
name of an image and returns a list of the comments stored for that image.

There is a procedure 'add_comment' that takes two arguments, the name of an
image and a comment as a string. The comment is stored in the database associated
with this image. 

There is a procedure 'list_images' that takes a single argument 'n' and returns a list of 
the most recent 'n' images that have been uploaded along with their details.  The return
value will be a list of tuples with one tuple per image, each tuple will contain four
elements: (path, date, owner, comments).  'path' is the path to the image relative to 
the default image directory, 'date' is a date string, 'owner' is the id of the owner
of the image and 'comments' is a list of comment strings for this image.

There is a procedure 'add_image' which takes two arguments, the name of an image
file and the email address of the owner of the image.  The image name is stored
in the database along with the owner id and the current date.   



Login
-----

As a visitor to the site, when I load the home page I see text boxes that have the
placeholder text 'username' and 'password' and a button labelled 'Login'. 

As a registered user, when I enter my username and password into the text boxes and press
"Login", in the page returned I see a message "Welcome X" where X is my full name. 

As a registered user, when I enter my username but the wrong password into the text
boxes and press "Login", the page returned contains the message "Incorrect username or
password" and allows me to re-enter my details and try again.

As a registered user, once I have logged in, I notice that every page that I visit
on the site contains my name next to a button labelled "Logout".  Also, if I leave 
the site and then reload the home page from a saved link, my name is still shown.

As a registered user, when I click on the "Logout" button on a page, the page returned
is the default home page with the "Welcome to FlowTow" banner and the login form and
the URL of the page is that of the home page. 

	Note that all of this can be done without a database by _mocking_ the interface that
	checks a password (eg. it returns true for a fixed password). It would require 
	a cookie for persistence of a session - again the session lookup would have
	to be mocked to return a fixed user for the session key.
	
	
Upload Images 
----------------

As a logged in user, on the home page I see a form that allows me to choose an image
file to upload with a button labelled "Upload Image".

As a visitor to the site, when I am not logged in, I do not see a form to upload an image.

As a logged in user, when I select a file and click "Upload Image" the page returned
contains my image as the first one on the page. Below the image is the date and 
my name. 


Storing Files and Records
-------------------------

As a logged in user, when I upload a second image via the form on the main page, 
the page that is returned contains both of my images with the date and my name
below them. 

As a logged in user, when another logged in user uploads an image and I refresh 
the home page, I see the most recent image displayed above my older images. 

As a visitor to the site, when I reload the home page I see the most recent
three images displayed with the date and name of the photographer. 

As a logged in user, when I load the home page I see a link with the title "My FowTows". 
When I click on this link the page that is returned contains a list of the titles
of all of the images I have uploaded. Each title is a hyperlink.







