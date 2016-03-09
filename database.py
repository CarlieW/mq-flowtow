'''
Created on Mar 26, 2012

@author: steve
'''

import sqlite3
import random

class COMP249Db():
    '''
    Provide an interface to the database for a COMP249 web application
    '''


    def __init__(self, dbname="comp249.db"):
        '''
        Constructor
        '''

        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname)
        ### ensure that results returned from queries are strings rather
        # than unicode which doesn't work well with WSGI
        self.conn.text_factory = str

    def cursor(self):
        """Return a cursor on the database"""

        return self.conn.cursor()

    def commit(self):
        """Commit pending changes"""

        self.conn.commit()

    def delete(self):
        """Destroy the database file"""
        pass


    def encode(self, password):
        """Return a one-way hashed version of the password suitable for
        storage in the database"""

        import hashlib, binascii

        salt = b'salt should be a random string'
        dk = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), salt, 100000)
        return binascii.hexlify(dk).decode('utf-8')


    def create_tables(self):
        """Create and initialise the database tables
        This will have the effect of overwriting any existing
        data."""


        sql = """
DROP TABLE IF EXISTS users;
CREATE TABLE users (
           nick text unique primary key,
           password text,
           avatar text
);

DROP TABLE IF EXISTS sessions;
CREATE TABLE sessions (
            sessionid text unique primary key,
            usernick text,
            FOREIGN KEY(usernick) REFERENCES users(nick)
);

DROP TABLE IF EXISTS images;
CREATE TABLE images (
            filename text unique primary key,
            timestamp text default CURRENT_TIMESTAMP,
            usernick text,
            FOREIGN KEY(usernick) REFERENCES users(nick)
);

DROP TABLE IF EXISTS likes;
CREATE TABLE likes (
            filename text,
            usernick text,
            FOREIGN KEY(usernick) REFERENCES users(nick),
            FOREIGN KEY(filename) REFERENCES images(filename)
);"""

        self.conn.executescript(sql)
        self.conn.commit()


    def sample_data(self):
        """Generate some sample data for testing the web
        application. Erases any existing data in the
        database"""

                    #  pass,   nick             avatar
        self.users = [('bob', 'Bobalooba', 'http://robohash.org/bob'),
                      ('jim', 'Jimbulator', 'http://robohash.org/jim'),
                      ('mary', 'Contrary', 'http://robohash.org/mary'),
                      ('jb', 'Bean', 'http://robohash.org/jb'),
                      ('mandible', 'Mandible', 'http://robohash.org/mandible'),
                      ('bar', 'Barfoo', 'http://robohash.org/bar'),
        ]
        #  Robots lovingly delivered by Robohash.org


        # filename, date, useremail, comments
        self.images = [
                   ('cycling.jpg',     '2015-02-20 01:45:06', 'Bobalooba', ['Bean', 'Barfoo', 'Mandible']),
                   ('window.jpg',      '2015-02-20 00:54:53', 'Jimbulator', ['Bobalooba', 'Bean']),
                   ('hang-glider.jpg', '2015-02-19 20:43:48', 'Bobalooba', ['Jimbulator', 'Barfoo']),
                   ('seashell.jpg',    '2015-02-19 19:03:22', 'Contrary', [])
                 ]


        # create one entry per image for each user
        cursor = self.cursor()
        # create one entry for each user
        for password, nick, avatar in self.users:
            sql = "INSERT INTO users (nick, password, avatar) VALUES (?, ?, ?)"
            cursor.execute(sql, (nick, self.encode(password), avatar))

        for fname, date, nick, likers in self.images:
            sql = 'INSERT INTO images (filename, timestamp, usernick) VALUES (?, ?, ?)'

            # now create the database entry for this image
            cursor.execute(sql, (fname, date, nick))

            # and create some likes for this image
            sql = "INSERT INTO likes (filename, usernick) VALUES (?, ?)"

            for user in likers:
                cursor.execute(sql, (fname, user))

            # and one anonymous like

            cursor.execute(sql, (fname, None))

        # commit all updates to the database
        self.commit()


if __name__=='__main__':
    # if we call this script directly, create the database and make sample data
    db = COMP249Db()
    db.create_tables()
    db.sample_data()
