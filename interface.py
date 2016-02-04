'''
Created on Mar 28, 2014

@author: steve
'''
import datetime


def list_comments(db, filename):
    """Return a list of the comments stored for this image filename"""
    
    cursor = db.cursor()
    
    cursor.execute("select comment from comments where filename=?", (filename,))
    result = []
    for row in cursor:
        result.append(row[0])
    return result


def add_comment(db, filename, comment):
    """Add this comment to the database for this image filename"""
    
    print("ADD COMMENT", filename, comment)
    
    sql = "insert into comments values (?, ?)"
    
    cursor = db.cursor()
    cursor.execute(sql, (filename, comment))
    
    db.commit()
    
    
def list_images(db, n):
    """Return a list of tuples for the first 'n' images in 
    order of date.  Tuples should contain (filename, date, useremail, comments)."""
    
    sql = "select filename, date, useremail from images order by date desc limit ?"
    
    cursor = db.cursor()
    cursor.execute(sql, (n,))
    
    result = []
    for row in cursor:
        comments = list_comments(db, row[0])
        result.append((row[0], row[1], row[2], comments))
    return result

def list_only_images(db, n):
    """Return a list of tuples for the first 'n' images in 
    order of date.  Tuples should contain (filename, date, useremail)."""
    
    sql = "select filename, date, useremail from images order by date desc limit ?"
    
    cursor = db.cursor()
    cursor.execute(sql, (n,))
    
    return cursor.fetchall()



def list_images_for_user(db, useremail):
  """Return a list of tuples for the images belonging to this user.
    Tuples should contain (filename, date, useremail)."""
  
  sql = "select filename, date, useremail from images where useremail=? order by date desc"
  
  cursor = db.cursor()
  cursor.execute(sql, (useremail,))
  
  return cursor.fetchall()
    
    
    
def add_image(db, filename, useremail):
    """Add this image to the database for the given user"""
    
    sql = "insert into images values (?, ?, ?)"
    
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    
    cursor = db.cursor()
    cursor.execute(sql, (filename, date, useremail))
    
    db.commit()