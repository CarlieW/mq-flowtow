'''
Created on Mar 26, 2012

@author: steve
'''

import sqlite3

DATABASE_NAME = 'flowtow.db'


def encode(password):
    """Return a one-way hashed version of the password suitable for
    storage in the database"""

    import hashlib, binascii

    try:
        salt = b'salt should be a random string'
        dk = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), salt, 100000)
        return binascii.hexlify(dk).decode('utf-8')
    except:
        # if we don't have the pbkdf2_hmac module
        return hashlib.sha512(password.encode()).hexdigest()


def create_tables(db):
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

    db.executescript(sql)
    db.commit()


def sample_data(db):
    """Generate some sample data for testing the web
    application. Erases any existing data in the
    database"""

    #         password    nick          avatar
    users = [('bob',      'Bobalooba',  'http://robohash.org/bob'),
             ('jim',      'Jimbulator', 'http://robohash.org/jim'),
             ('mary',     'Contrary',   'http://robohash.org/mary'),
             ('jb',       'Bean',       'http://robohash.org/jb'),
             ('mandible', 'Mandible',   'http://robohash.org/mandible'),
             ('bar',      'Barfoo',     'http://robohash.org/bar'),
    ]
    #  Robots lovingly delivered by Robohash.org

    # filename, date, usernick, likes
    images = [
               ('cycling.jpg',     '2015-02-20 01:45:06', 'Bobalooba', ['Bean', 'Barfoo', 'Mandible']),
               ('window.jpg',      '2015-02-20 00:54:53', 'Jimbulator', ['Bobalooba', 'Bean']),
               ('hang-glider.jpg', '2015-02-19 20:43:48', 'Bobalooba', ['Jimbulator', 'Barfoo']),
               ('seashell.jpg',    '2015-02-19 19:03:22', 'Contrary', [])
             ]

    # create one entry per image for each user
    cursor = db.cursor()
    # create one entry for each user
    for password, nick, avatar in users:
        sql = "INSERT INTO users (nick, password, avatar) VALUES (?, ?, ?)"
        cursor.execute(sql, (nick, encode(password), avatar))

    for fname, date, nick, likers in images:
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
    db.commit()

    return users, images


if __name__=='__main__':
    # if we call this script directly, create the database and make sample data
    db = sqlite3.connect(DATABASE_NAME)
    create_tables(db)
    sample_data(db)
