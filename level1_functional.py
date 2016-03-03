'''
Created on Mar 3, 2014

@author: steve
'''
import unittest
from webtest import TestApp
import main
import bottle

class Level1FunctionalTests(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(main.application)
        bottle.debug() # force debug messages in error pages returned by webtest

    def tearDown(self):
        pass

    def testHomepage(self):
        """As a visitor to the site, when I load the
         home page I see a banner with "Welcome to FlowTow"."""

        result = self.app.get('/')
        self.assertIn("Welcome to FlowTow", result)


    def testImagesPresent(self):
        """As a visitor to the site, when I load the home page I
        see three images displayed, each
        labelled with a date, a user name and a title. """

        result = self.app.get('/')

        images = result.html.find_all('img')

        # expect to find three images
        self.assertEqual(3, len(images), "Wrong number of images found")

        flowtows = result.html.find_all(class_='flowtow')

        self.assertEqual(3, len(flowtows))

        # each contains the image (check for like form in another test)
        for index in range(3):
            div = flowtows[index]

            # should contain elements with class 'user', 'date' and 'likes'
            self.assertNotEqual([], div.find_all(class_='user'), "can't find element with class 'user' in flowtow div")
            self.assertNotEqual([], div.find_all(class_='date'), "can't find element with class 'date' in flowtow div")
            self.assertNotEqual([], div.find_all(class_='likes'), "can't find element with class 'likes' in flowtow div")

            # look for just one image
            img = div.find_all('img')
            self.assertEqual(1, len(img))

            # can we actually get the image
            # find the URL
            url = img[0]['src']
            # try requesting it and test the content-type header returned
            newresult = self.app.get(url)
            self.assertEqual('image/jpeg', newresult.content_type)

    def testImageLikeForms(self):
        """As a visitor to the site, when I load the home page I see a button below each image with the text "Like".

        The button is part of a form that submits a like request. The action of the form should be /like,
        the form should have a hidden field called filename containing the filename of the image being liked
        and the button should be the submit button in the from.
        """

        result = self.app.get('/')

        flowtows = result.html.find_all(class_='flowtow')

        # each contains the form for liking images
        for div in flowtows:

            forms = div.find_all('form')
            self.assertEqual(len(forms), 1, "expected one form in image div:\n\n%s" % str(div))

            form = forms[0]

            # look for two inputs
            inputs = form.find_all('input')
            self.assertGreater(len(inputs), 1, "Expected at least two input fields (filename and submit) in: \n\n%s" % str(div))

            # check that the submit input has the right attributes
            for i in inputs:
                if i['type'] == 'submit':
                    self.assertEqual('Like', i['value'], "submit button on the form should have the value 'Like'")

            self.assertEqual(form['action'], '/like', "form action should be /like")


    def testAboutSiteLink(self):
        """As a visitor to the site, when I load the home page I see a link to another page
called "About this site".
"""


        result = self.app.get('/')
        links = result.html.find_all('a')

        self.assertTrue(any(['About' in l.text for l in links]), "Can't find 'About this site' link")



    def testAboutSitePage(self):
        """As a visitor to the site, when I click on the link "About this site" I am taken to
a page that contains the site manifesto, including the words "FlowTow is a new, exciting,
photo sharing service like nothing you've seen before!"
        """

        message = "FlowTow is a new, exciting, photo sharing service like nothing you've seen before!"

        result = self.app.get('/')

        newresult = result.click(description="About")

        # now look for our message in the page
        self.assertIn(message, newresult)

    def testPageCSS(self):
        """As a visitor to the site, I notice that all the pages on the site have the same
design with the same colours and fonts used throughout.
        Interpret this as having a CSS file linked in the pages"""

        result = self.app.get('/')
        links = result.html.find_all('link', rel='stylesheet')

        self.assertGreater(len(links), 0, "No CSS stylesheet linked to home page")



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
