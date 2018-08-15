# -*- coding: UTF-8 -*-
from selenium import webdriver
import unittest,time
class MyTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.youdao.com"
    def test_youdao(self):
        driver = self.driver
        driver.get(self.base_url+'/')
        driver.find_element_by_id('translateContent').clear()
        driver.find_element_by_id('translateContent').send_keys('webdriver')
        driver.find_element_by_link_text(u'翻译').click()
        time.sleep(2)
        title = driver.title
        self.assertEqual(title, u'在线翻译_有道')
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()