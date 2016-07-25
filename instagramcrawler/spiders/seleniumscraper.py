#!/usr/bin/env python3

import requests
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class InstagramCrawler:
    def __init__(self, driver, data):
        self.data = data
        #profile = webdriver.FirefoxProfile("/home/paradox/.mozilla/firefox/cb0shu16.default/") self.driver = webdriver.Firefox()
        self.driver = driver
        self.url_login = "https://www.instagram.com/accounts/login/?force_classic_login"
        self.numbers = []
        self.followers = []
        self.following = []

    def login(self):
        self.driver.get(self.url_login)

        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(self.data['USERNAME'])
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(self.data['PASSWORD'])
        self.driver.find_element_by_xpath("//input[@type='submit']").click()

        # Wait for the login page to load
        try:
            WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Instagram"))
                )
        except:
            print("oh shit!!!!")
        return
        """
        try:
            self.driver.set_page_load_timeout(1)
        except Exception:
            return
        """

    def login_simple(self):
        headers = {'user-agent' : "Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0" }
        response = requests.post(self.url_login, data={'username' : self.data['USERNAME'], 'password' : self.data['PASSWORD'] }, headers=headers )
        print(response.status_code)

    # simulate click
    def __click(self, scrape_type="follower"):
        print("-"*30, scrape_type)
        self.driver.find_element_by_partial_link_text(scrape_type).click()

        # Wait for the followers modal to load
        xpath = "//div[@style='position: relative; z-index: 1;']/div/div[2]/div/div[1]"
        followers_elems = []
        WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, xpath)))

        xp = "//div[@style='position: relative; z-index: 1;']//ul"
        self.driver.find_element_by_xpath(xp).click()

        # scrolling stuffs by simulating the "END" button
        index = 1 if scrape_type=="follower" else 2
        for i in range(int((self.numbers[index]-10)/9) + 2):
            print("scrolling...{}".format(scrape_type))
            time.sleep(3)
            self.driver.find_element_by_xpath(xp).send_keys(Keys.END)

        # Finally, scrape the followers/following accordingly
        xpath = "//div[@style='position: relative; z-index: 1;']//ul/li/div/div/div/div/a"
        elems = self.driver.find_elements_by_xpath(xpath)
        return [e.text for e in elems]


    def scrape(self):
        self.driver.get("https://www.instagram.com/{0}/".format(self.data['USERNAME']))

        # get elements for no. of posts/followers/following
        numbers = self.driver.find_elements_by_xpath("//span[@class='_bkw5z _kjym7']")
        self.numbers = [ int(elem.text) for elem in numbers ]
        
        # get username of all the followers
        self.followers = self.__click("follower")
        
        # close the modal
        self.driver.find_elements_by_xpath("//button[@class='_3eajp']")[0].click()

        # get username of all the following
        self.following = self.__click("following")

    def run(self):
        self.login()
        self.scrape()


def main():
    pass

if __name__ == "__main__":
    main()

