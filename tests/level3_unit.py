'''
Created on Mar 26, 2012

@author: steve
'''

import unittest
import sqlite3
from http.cookies import SimpleCookie
from bottle import request, response

# import the module to be tested
import users
import model
import database


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

    def test_list_images_user(self):
        """Test that list_images with the extra usernick argument
         returns the right list of images for a user"""

        for password, nick, avatar in self.users:

            # get the three most recent image entries
            image_list = model.list_images(self.db, 3, nick)
        
            # image_list should be a list of dictionaries
            for img in image_list:
                self.assertEqual(dict, type(img), "returned element not a dictionary")
        

            # check that the images are in the right order
            dates = [img['timestamp'] for img in image_list]
            sorteddates = [img['timestamp'] for img in image_list]
            sorteddates.sort(reverse=True)
            self.assertListEqual(dates, sorteddates)

            # and the owners, dates and like count are correct
            for img in image_list:
                for refimage in self.images:
                    if img['filename'] == refimage[0]:
                        self.assertEqual(refimage[1], img['timestamp'])
                        self.assertEqual(refimage[2], img['user'])
                        self.assertEqual(len(refimage[3])+1, img['likes'])

    def test_check_login(self):


        for password, nick, avatar in self.users:
            # try the correct password
            self.assertTrue(users.login(self.db, nick, password), "Password check failed for user %s" % nick)

            # and now incorrect
            self.assertFalse(users.login(self.db, nick, "badpassword"), "Bad Password check failed for user %s" % nick)

        # check for an unknown email
        self.assertFalse(users.login(self.db, "whoisthis", "badpassword"), "Bad Password check failed for unknown user")

    def get_cookie_value(self, cookiename):
        """Get the value of a cookie from the bottle response headers"""

        headers = response.headerlist
        for h,v in headers:
            if h == 'Set-Cookie':
                cookie = SimpleCookie(v)
                if cookiename in cookie:
                    return cookie[cookiename].value

        return None

    def test_delete_session(self):
        """The delete_session procedure should remove all sessions for
        a given user in the sessions table.
        Test relies on working generate_session"""

        # run tests for all test users
        for passwd, nick, avatar in self.users:

            # now remove the session
            users.logout()

    def test_session_user(self):
        """The session_user procedure finds the name of the logged in
        user from the session cookie if present

        Test relies on working generate_session
        """

        # first test with no cookie
        nick_from_cookie = users.session_user(self.db)
        self.assertEqual(nick_from_cookie, None, "Expected None in case with no cookie, got %s" % str(nick_from_cookie))

        request.cookies['beaker.session.id'] = 'fake sessionid'
        nick_from_cookie = users.session_user(self.db)

        self.assertEqual(nick_from_cookie, None, "Expected None in case with invalid session id, got %s" % str(nick_from_cookie))

        # run tests for all test users
        for password, nick, avatar in self.users:

            users.login(self.db, nick, password)

            sessionid = self.get_cookie_value('beaker.session.id')

            request.cookies['beaker.session.id'] = sessionid

            nick_from_cookie = users.session_user(self.db)

            self.assertEqual(nick_from_cookie['nick'], nick)




if __name__ == "__main__":
    unittest.main()