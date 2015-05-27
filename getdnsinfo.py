#coding=utf-8
__author__ = 'Administrator'



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re,sys


reload(sys)
sys.setdefaultencoding('utf8')


class Untitled(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://172.20.2.254:8080/"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("signin_username").clear()
        driver.find_element_by_id("signin_username").send_keys("")
        driver.find_element_by_id("signin_password").clear()
        driver.find_element_by_id("signin_password").send_keys("")
        driver.find_element_by_css_selector("button.btn").click()
        self.verificationErrors = []
        self.accept_next_alert = True

    def logMessage(self,message):
        fp = open('dnsres.txt','a')
        fp.writelines(time.strftime("%Y-%m-%d %H:%M:%S") + message +'\n')
        fp.close()

    def test_untitled(self):
        driver = self.driver
        # driver.find_element_by_xpath("//div[@id='ext-gen4']/div/span/div[2]/a/span").click()
        driver.get(self.base_url + '/index.php/dnsproxy')
        aa = driver.find_element_by_css_selector("div.explain-con").text

        while True:
            driver.refresh()
            aa =driver.find_element_by_css_selector("div.explain-con").text
            self.logMessage(aa)
        # self.assertEqual(u"当前 8 请求/秒", driver.find_element_by_css_selector("div.explain-con").text)



    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    # def is_alert_present(self):
    #     try: self.driver.switch_to_alert()
    #     except NoAlertPresentException, e: return False
    #     return True
    #
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
