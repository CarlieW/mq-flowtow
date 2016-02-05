'''
Created on Mar 3, 2014

@author: steve
'''
import unittest
from webtest import TestApp
import main
import mock

class Level1FunctionalTests(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(main.application)

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

        image_list = mock.list_images(3)

        self.assertEqual(3, len(flowtows))

        # each contains the image, date, author and comments
        for index in range(3):
            div = flowtows[index]
            (path, date, user, comments) = image_list[index]

            self.assertIn(date, div.text)
            self.assertIn(user, div.text)
            for c in comments:
                self.assertIn(c, div.text)

            # look for just one image
            img = div.find_all('img')
            self.assertEqual(1, len(img))

            # can we actually get the image
            # find the URL
            url = img[0]['src']
            # try requesting it and test the content-type header returned
            newresult = self.app.get(url)
            self.assertEqual('image/jpeg', newresult.content_type)

    def testImageCommentForms(self):
        """As a visitor to the site, when I load the home page I see a comment form below each
image with the placeholder text "Enter your comment here" and a button labelled "Submit"
        """

        result = self.app.get('/')

        flowtows = result.html.find_all(class_='flowtow')

        # each contains the form for comments
        for div in flowtows:
            # look for two inputs
            inputs = div.find_all('input')
            self.assertGreater(len(inputs), 1, "Expected at least two input fields (comment and submit)")

            # check that the required inputs have the right attributes
            for i in inputs:
                if i['type'] == 'submit':
                    self.assertEqual('Submit', i['value'])
                elif i['name'] == 'comment':
                    self.assertEqual('Enter your comment here', i['placeholder'])



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
