FlowTow Image Sharing
===

This project implements a simple photo sharing site as an example for learning the basics
of web development.  It accompanies my notes on [Python Web Programming](http://pwp.stevecassidy.net).

The project uses [bottle](https://bottlepy.org) as a web framework, the
[beaker](https://beaker.readthedocs.io/en/latest/index.html) plugin to handle
user sessions and the [bottle-sqlite](https://bottlepy.org/docs/0.12/plugins/sqlite.html)
plugin to implement the database interface.  

The app displays a list of uploaded images.  Users must login to post images 
and each user can see a page containing their own images.  Each image has a 'like' 
button and you can like an image whether logged in or not.  The number of likes
is displayed with each image. 

