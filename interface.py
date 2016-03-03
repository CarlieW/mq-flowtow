'''
Created on Mar 28, 2014

@author: steve
'''


def list_images(db, n, usernick=None):
    """Return a list of dictionaries for the first 'n' images in
    order of timestamp. Each dictionary will contain keys 'filename', 'timestamp', 'user' and 'comments'.
    The 'comments' value will be a list of comments associated with this image (as returned by list_comments).
    If usernick is given, then only images belonging to that user are returned."""

    cursor = db.cursor()

    if usernick is None:
        sql = "select images.filename, timestamp, usernick from images order by timestamp desc limit ?"
        cursor.execute(sql, (n,))

    else:
        sql = "select images.filename, timestamp, usernick from images where usernick=? order by timestamp desc limit ?"
        cursor.execute(sql, (usernick, n))


    result = []
    for row in cursor:
        rowdict = {'filename': row[0], 'timestamp': row[1], 'user': row[2], 'likes': count_likes(db, row[0])}
        result.append(rowdict)

    return result



def add_image(db, filename, usernick):
    """Add this image to the database for the given user"""


    cursor = db.cursor()

    sql = "insert into images (filename, usernick) values (?, ?)"

    cursor.execute(sql, (filename, usernick))

    db.commit()


def add_like(db, filename, usernick=None):
    """Increment the like count for this image"""

    cursor = db.cursor()

    # validate the user
    if usernick != None:
        sql = "select nick from users where nick=?"
        cursor.execute(sql, (usernick,))

        # if there is no result from the query, return without adding the like
        if not cursor.fetchone():
            return

    # validate the filename
    sql = "select filename from images where filename=?"
    cursor.execute(sql, (filename,))

    # if there is no result from the query, return without adding the like
    if not cursor.fetchone():
        return

    sql = "insert into likes (filename, usernick) values (?, ?)"

    cursor.execute(sql, (filename, usernick))
    db.commit()


def count_likes(db, filename):
    """Count the number of likes for this filename"""

    cursor = db.cursor()
    cursor.execute("select count(filename) from likes where filename=?", (filename,))

    return cursor.fetchone()[0]