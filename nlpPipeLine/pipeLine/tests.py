from django.test import TestCase

import unittest
from selenium import webdriver
from django.test import Client



class TestSignup(unittest.TestCase):

    def test_signup_fire(self):
        c = Client()
        c.get("http://127.0.0.1:8000/", {'queryset': '',
                                         'for_submit': "Submit",
                                         'input': 'asd',
                                         'output': ''})

# class TestSignup(unittest.TestCase):
#
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#
#     def test_signup_fire(self):
#         self.driver.get("http://127.0.0.1:8000/")
#         self.driver.find_element_by_id('input').send_keys("test input text")
#         self.driver.find_element_by_id('submit').click()
#         self.assertIn("http://127.0.0.1:8000/", self.driver.current_url)
#
#     def tearDown(self):
#         self.driver.quit
#
if __name__ == '__main__':
     unittest.main()