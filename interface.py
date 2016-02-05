'''
Created on Mar 28, 2014

@author: steve
'''

def list_comments(db, filename):
    """Return a list of the comments stored for this image filename"""

    cursor = db.cursor()

    cursor.execute("select comment from comments where filename=?", (filename,))
    result = []
    for row in cursor:
        result.append(row[0])
    return result


def add_comment(db, filename, comment, usernick):
    """Add this comment to the database for this image filename"""

    sql = "insert into comments (filename, comment, usernick) values (?, ?, ?)"

    cursor = db.cursor()
    cursor.execute(sql, (filename, comment, usernick))

    db.commit()


def list_images(db, n):
    """Return a list of tuples for the first 'n' images in
    order of timestamp.  Tuples should contain (filename, timestamp, usernick, comments)."""

    sql = "select filename, timestamp, usernick from images order by timestamp desc limit ?"

    cursor = db.cursor()
    cursor.execute(sql, (n,))

    result = []
    for row in cursor:
        comments = list_comments(db, row[0])
        result.append((row[0], row[1], row[2], comments))
    return result

def list_only_images(db, n):
    """Return a list of tuples for the first 'n' images in
    order of timestamp.  Tuples should contain (filename, timestamp, usernick)."""

    sql = "select filename, timestamp, usernick from images order by timestamp desc limit ?"

    cursor = db.cursor()
    cursor.execute(sql, (n,))

    return cursor.fetchall()



def list_images_for_user(db, usernick):
  """Return a list of tuples for the images belonging to this user.
    Tuples should contain (filename, timestamp, usernick)."""

  sql = "select filename, timestamp, usernick from images where usernick=? order by timestamp desc"

  cursor = db.cursor()
  cursor.execute(sql, (usernick,))

  return cursor.fetchall()



def add_image(db, filename, usernick):
    """Add this image to the database for the given user"""

    sql = "insert into images (filename, usernick) values (?, ?, ?)"

    cursor = db.cursor()
    cursor.execute(sql, (filename, usernick))

    db.commit()
