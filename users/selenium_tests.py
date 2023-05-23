import time
import os
from faker import Faker
from selenium import webdriver
import unittest

from selenium.webdriver.common.by import By

fake = Faker()

USERNAME = "danylo_v"
PASSWORD = "$43Z4Km1$"
TEST_TITLE = fake.word()
TEST_CONTENT = fake.sentence()
TEST_COMMENT = fake.sentence()

class BlogTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(f'{os.getcwd()}//chromedriver.exe')

    def test_blog_scenario(self):
        # Вхід до акаунту
        self.browser.get('http://localhost:8000/users/login')
        self.browser.find_element(value='id_username').send_keys(USERNAME)
        self.browser.find_element(value='id_password').send_keys(PASSWORD)
        self.browser.find_element(by=By.CSS_SELECTOR, value='body > main > form > button').click()

        # Створення публікації
        self.browser.get('http://localhost:8000/posts/post/new')
        time.sleep(5)
        self.browser.find_element(by=By.NAME, value='title').send_keys(TEST_TITLE)
        self.browser.find_element(by=By.NAME, value='content').send_keys(TEST_CONTENT)
        self.browser.find_element(by=By.CSS_SELECTOR, value='body > main > form > button').click()
        new_post = self.browser.current_url

        # Перегляд публікацій
        self.browser.get('http://localhost:8000/posts/posts')

        # Створення коментаря
        self.browser.get(new_post)
        self.browser.find_element(by=By.LINK_TEXT, value='Add comment').click()
        self.browser.find_element(by=By.NAME, value='content').send_keys(TEST_COMMENT)
        self.browser.find_element(by=By.XPATH, value='/html/body/form/button').click()
        print("All tests are passed!")

    def tearDown(self):
        self.browser.quit()

if __name__ == '__main__':
    unittest.main()