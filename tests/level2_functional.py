'''
Created on Mar 3, 2014

@author: steve
'''
import unittest
from webtest import TestApp
import re
from urllib.parse import urlparse

import bottle
from bottle.ext import sqlite, beaker
import os
import sqlite3

import main

import database


DATABASE_NAME = "test.db"
main.app.install(sqlite.Plugin(dbfile=DATABASE_NAME))

# make sure bottle looks for templates in the main directory, not this one
bottle.TEMPLATE_PATH = [os.path.join(os.path.dirname(__file__), p) for p in ['../', '../views/']]


class Level2FunctionalTests(unittest.TestCase):

    def setUp(self):

        session_opts = {
            'session.type': 'memory',
        }
        beaker_app = beaker.middleware.SessionMiddleware(main.app, session_opts)
        db = sqlite3.connect(DATABASE_NAME)
        database.create_tables(db)
        self.users, self.images = database.sample_data(db)
        self.app = TestApp(beaker_app)
        bottle.debug() # force debug messages in error pages returned by webtest

    def tearDown(self):
        pass

    def testImagesPresent(self):
        """As a visitor to the site, when I load the home page I
        see three images displayed, each
        labelled with a date, a user name and a title. """

        result = self.app.get('/')

        images = result.html.find_all('img')

        # expect to find three images
        self.assertEqual(3, len(images), "Wrong number of images found")

        flowtows = result.html.find_all(class_='flowtow')

        image_list = self.images

        self.assertEqual(3, len(flowtows))

        # each contains the image, date, author and likes
        for index in range(3):
            div = flowtows[index]
            (path, date, user, likes) = image_list[index]

            self.assertIn(date, div.text)
            self.assertIn(user, div.text)
            # look for the number of likes
            self.assertIn(str(len(likes)+1), div.text, "expected to find %d likes mentioned in:\n\n%s" % (len(likes), div))

            # look for just one image
            img = div.find_all('img')
            self.assertEqual(1, len(img))

    def testLikeImage(self):
        """As a visitor to the site, when I click on "Like" below an image,
        the page refreshes and has one more like added to the total for that image."""

        response = self.app.get('/')
        originallikes = get_page_likes(response)

        print(originallikes)

        # find a form with the action /like
        for i in response.forms:
            form = response.forms[i]
            if form.action == '/like':

                self.assertIn('filename', form.fields, 'image like form does not have a filename field')


                filename = form['filename'].value

                formresponse = form.submit()

                # response should be a redirect to the main page
                self.assertIn(formresponse.status, ['303 See Other', '302 Found'])
                (_, _, path, _, _, _) = urlparse(formresponse.headers['Location'])
                self.assertEqual('/', path)

                # and the main page should now have one more like for this image
                newresponse = self.app.get('/')
                newlikes = get_page_likes(newresponse)

                print(newlikes)

                for key in originallikes.keys():
                    if key == filename:
                        self.assertEqual(originallikes[key]+1, newlikes[key])
                    else:
                        self.assertEqual(originallikes[key], newlikes[key])

                # we only need to test one form
                break


def get_page_likes(response):
    """Scan a page and create a dictionary of the image filenames
    and displayed like count for each image. Return the
    dictionary."""

    # find all flowtow divs
    flowtows = response.html.find_all('div', class_='flowtow')
    result = dict()
    for div in flowtows:
        # get the filename from the form hidden input
        input = div.find("input", attrs={'name': "filename"})

        filename = input['value']

        # find the likes element
        likesel = div.find(class_='likes')
        # grab the integer from this element
        m = re.search('\d+', likesel.text)
        if m:
            likes = int(m.group())
        else:
            likes = 0

        result[filename] = likes

    return result



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
