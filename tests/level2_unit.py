'''
Created on Mar 3, 2014

@author: Steve Cassidy

'''
import datetime
import unittest
import sqlite3
from bottle import request

import database
import model


class MockBeakerSession(dict):
    """A Mock version of a beaker session, just a dictionary
    with a 'save' method that does nothing"""

    def save(self):
        pass

    def delete(self):
        pass


class Test(unittest.TestCase):

    def setUp(self):
        # init an in-memory database
        self.db = sqlite3.connect(':memory:')
        self.db.row_factory = sqlite3.Row

        database.create_tables(self.db)
        self.users, self.images = database.sample_data(self.db)
        if 'beaker.session' in request.environ:
            del request.environ['beaker.session']

        request.environ['beaker.session'] = MockBeakerSession({})

    def test_list_images(self):
        """Test that list_images returns the right list of images"""

        # get the four most recent image entries
        image_list = model.list_images(self.db, 4)

        self.assertEqual(4, len(image_list))
        # and all entries are four elements long
        self.assertTrue(all([len(i) == 4 for i in image_list]))

        # check that the images are in the right order
        self.assertListEqual([img[0] for img in self.images], [img['filename'] for img in image_list])

        # and the dates are right
        self.assertListEqual([img[1] for img in self.images], [img['timestamp'] for img in image_list])

        # and the owners
        self.assertListEqual([img[2] for img in self.images], [img['user'] for img in image_list])

        # now check the likes
        for image in image_list:
            likes = [img[3] for img in self.images if img[0] == image['filename']]
            self.assertEqual(len(likes[0])+1, image['likes'])



    def test_add_image(self):
        """Test that add_image updates the database properly"""

        imagename = 'new.jpg'
        usernick = 'carol'
        model.add_image(self.db, imagename, usernick)

        images = model.list_images(self.db, 5)

        self.assertEqual(imagename, images[0]['filename'], 'wrong image name after add_image')
        self.assertEqual(usernick, images[0]['user'], 'wrong user in first image')
        # date should be today's
        today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        date = images[0]['timestamp']
        self.assertEqual(date[:10], today)


    def test_count_likes(self):
        """Test that count_likes correctly counts the likes for an image"""

        for image in self.images:

            count = model.count_likes(self.db, image[0])

            # expect the listed users plus one anonymous like
            self.assertEqual(len(image[3])+1, count)


        # for a non-existent image, count_likes returns zero

        self.assertEqual(0, model.count_likes(self.db, "imagethatdoesntexist.jpg"))



    def test_add_like(self):
        """Test that add_like can add a like either anonymously or from another user"""

        filename = self.images[0][0]

        # anonymous like
        count = model.count_likes(self.db, filename)

        model.add_like(self.db, filename)

        self.assertEqual(count + 1, model.count_likes(self.db, filename), "anonymous like not added")

        # a like from a user
        model.add_like(self.db, filename, self.users[3][1])

        self.assertEqual(count + 2, model.count_likes(self.db, filename), "like for known user not added")

        # like from an unknown user should not be stored
        model.add_like(self.db, filename, 'Imposter')

        self.assertEqual(count + 2, model.count_likes(self.db, filename), "you counted like from unknown user")

        # like of an unknown image should not be stored
        model.add_like(self.db, 'unknownfile.jpg', self.users[3][1])

        self.assertEqual(0, model.count_likes(self.db, 'unknownfile.jpg'), "you counted like from unknown file")






if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
