'''
Created on Mar 3, 2014

@author: steve
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import datetime
import os

import interface
from urllib.request import urlopen

class Level3FunctionalTests(unittest.TestCase):

    base_url = 'http://localhost:8000/'
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.close()
            
    def doLogin(self, email, password):
        """Perform a login with some validation along the way"""
        
        driver = self.driver
        
        # there is a form with id='loginform'
        try:
            loginform = driver.find_element_by_id('loginform')
        except NoSuchElementException:
            self.fail("no form with id='loginform' found")
 
        # login form action should be /login
        self.assertEqual(self.base_url + 'login', loginform.get_attribute('action'), "login form action should be '/login'")
 
        # the form has an email field
        try:
            emailfield = loginform.find_element_by_name('email')
        except NoSuchElementException:
            self.fail("no email field found for login form")
        
        # and a password field
        try: 
            passwordfield = loginform.find_element_by_name('password')
        except NoSuchElementException:
                self.fail("no password field found for login form")
                
        self.assertEqual(passwordfield.get_attribute('type'), 'password', "Password field should have type='password'")                
                
        emailfield.send_keys(email)
        passwordfield.send_keys(password)
        # submit the form
        loginform.submit()
        
                        
                

    def testMyImages(self):
        """As a registered user, when I load the "My Images" page (http://localhost:8000/my) I see 
        a form that has a file selection input and a button labelled "Upload Image". 
        
        As a registered user, when I load the "My Images" page and select a file and then click 
        on the "Upload Image" button my image file is uploaded to the site. The page that is 
        returned is the "My Images" page and the newly uploaded image is the first image on the page.
        
        """
        
        driver = self.driver
        driver.get(self.base_url)
         
        # fill out the form
        email = 'bob@here.com'
        password = 'bob'
        
        self.doLogin(email, password)
        
        # expect to see link to my images
        try:
            imagelink = driver.find_element_by_link_text('My Images')        
        except NoSuchElementException:
            self.fail("can't find link to My Images page")
            
        imagelink.click()
        
        # find a file upload form
        try:
            form = driver.find_element_by_id('uploadform')
        except NoSuchElementException:
            self.fail("No form found with id='uploadform")

        self.assertEqual(self.base_url + 'upload', form.get_attribute('action'), "upload form action should be '/upload'")

        try:
            fileinput = form.find_element_by_tag_name('input')
        except NoSuchElementException:
            self.fail("No input field in upload form")

        self.assertEqual(fileinput.get_attribute('type'), 'file')

        # now try uploading a file
        fileinput.click()
        newimage = os.path.join(os.path.dirname(__file__), "flower.jpg")
        fileinput.send_keys(newimage)
        form.submit()
    
        # now need to check that our image appears first in the page
        
        divs = driver.find_elements_by_class_name('flowtow')
        
        self.assertGreater(1, len(divs), "expected at least one 'flowtow' div in page")
        
        img = divs[0].find_elements_by_tag_name('img')
        self.assertEqual("flower.jpg", img.get_attribute('src'))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main(warnings='ignore')