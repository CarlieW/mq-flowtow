'''
Created on Mar 3, 2014

@author: Steve Cassidy

Version 2: adds test for list_only_images, a simplified version of list_images

'''
import unittest
import datetime
import random

import interface
from database import COMP249Db


class Level2UnitTests(unittest.TestCase):


    def setUp(self):
        # open an in-memory database for testing
        self.db = COMP249Db(':memory:')
        self.db.create_tables()
        self.db.sample_data()
        self.images = self.db.images
        self.users = self.db.users



    def test_list_images(self):
        """Test that list_images returns the right list of images"""

        # get the four most recent image entries
        image_list = interface.list_images(self.db, 4)

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
        interface.add_image(self.db, imagename, usernick)

        images = interface.list_images(self.db, 5)

        self.assertEqual(imagename, images[0]['filename'], 'wrong image name after add_image')
        self.assertEqual(usernick, images[0]['user'], 'wrong user in first image')
        # date should be today's
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        date = images[0]['timestamp']
        self.assertEqual(date[:10], today)


    def test_count_likes(self):
        """Test that count_likes correctly counts the likes for an image"""

        for image in self.images:

            count = interface.count_likes(self.db, image[0])

            # expect the listed users plus one anonymous like
            self.assertEqual(len(image[3])+1, count)


        # for a non-existent image, count_likes returns zero

        self.assertEqual(0, interface.count_likes(self.db, "imagethatdoesntexist.jpg"))



    def test_add_like(self):
        """Test that add_like can add a like either anonymously or from another user"""

        filename = self.images[0][0]

        # anonymous like
        count = interface.count_likes(self.db, filename)

        interface.add_like(self.db, filename)

        self.assertEqual(count+1, interface.count_likes(self.db, filename), "anonymous like not added")

        # a like from a user
        interface.add_like(self.db, filename, self.users[3][1])

        self.assertEqual(count+2, interface.count_likes(self.db, filename), "like for known user not added")

        # like from an unknown user should not be stored
        interface.add_like(self.db, filename, 'Imposter')

        self.assertEqual(count+2, interface.count_likes(self.db, filename), "you counted like from unknown user")

        # like of an unknown image should not be stored
        interface.add_like(self.db, 'unknownfile.jpg', self.users[3][1])

        self.assertEqual(0, interface.count_likes(self.db, 'unknownfile.jpg'), "you counted like from unknown file")






if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
