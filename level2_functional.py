'''
Created on Mar 3, 2014

@author: steve
'''
import unittest
import webtest
import datetime

import main
import interface
from database import COMP249Db

class Level2FunctionalTests(unittest.TestCase):

    def setUp(self):
        self.app = webtest.TestApp(main.application)
        self.db = COMP249Db()
        self.db.create_tables()
        self.db.sample_data()


    def tearDown(self):
        pass


    def testSubmitCommentForms(self):
        """As a visitor to the site, when I load the home page I see a comment form below each
image with the placeholder text "Enter your comment here" and a button labelled "Submit"
        """

        testcomment = "This is a TEST Comment %s" % datetime.datetime.today()

        response = self.app.get('/')

        flowtows = response.html.find_all(class_='flowtow')
        self.assertEqual(len(flowtows), 3, "Expected three divs with class flowtow in page")

        # get the first div
        div = flowtows[0]

        # find the first form
        f = div.find_all('form')[0]

        # make a webtest form from this
        form = webtest.forms.Form(response, str(f))

        form['comment'] = testcomment

        response = form.submit()

        # response should be a redirect
        self.assertEqual('303 See Other', response.status)
        self.assertEqual('/', response.headers['Location'])

        # follow the redirect
        response = response.follow()

        # check that the comment is in the first flowtow div in the returned page

        divs = response.html.find_all(class_='flowtow')

        self.assertEqual(3, len(divs), "wrong number of flowtow divs in page")

        # look for the comment in the first
        self.assertIn(testcomment, divs[0].text)


    def testCommentMarkupQuoted(self):
        """As a visitor to the site, when I enter a comment that contains some HTML markup,
            the comment appears on the page with the HTML markup in quoted form.
        """

        testcomment = "Comment with <a href='http://example.com'>some markup</a> %s" % datetime.datetime.today()

        response = self.app.get('/')

        flowtows = response.html.find_all(class_='flowtow')
        self.assertEqual(len(flowtows), 3, "Expected three divs with class flowtow in page")

        # get the first div
        div = flowtows[0]

        # find the first form
        f = div.find_all('form')[0]

        # make a webtest form from this
        form = webtest.forms.Form(response, str(f))

        form['comment'] = testcomment

        response = form.submit()

        # response should be a redirect
        self.assertEqual('303 See Other', response.status)
        self.assertEqual('/', response.headers['Location'])

        # follow the redirect
        response = response.follow()

        # check that the comment is in the first flowtow div in the returned page

        divs = response.html.find_all(class_='flowtow')

        self.assertEqual(3, len(divs), "wrong number of flowtow divs in page")

        # look for the comment in the first, should see the exact string since markup should be quoted
        self.assertIn(testcomment, divs[0].text)




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
