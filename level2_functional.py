'''
Created on Mar 3, 2014

@author: steve
'''
import unittest
import webtest
import re
from urllib.parse import urlparse

import main
from database import COMP249Db

class Level2FunctionalTests(unittest.TestCase):

    def setUp(self):
        self.app = webtest.TestApp(main.application)
        self.db = COMP249Db()
        self.db.create_tables()
        self.db.sample_data()


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

        image_list = self.db.images

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

            # can we actually get the image
            # find the URL
            url = img[0]['src']
            # try requesting it and test the content-type header returned
            newresult = self.app.get(url)
            self.assertEqual('image/jpeg', newresult.content_type)


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
