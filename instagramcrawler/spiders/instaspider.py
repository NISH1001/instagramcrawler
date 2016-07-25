from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from scrapy.http.cookies import CookieJar
from scrapy.shell import inspect_response

from instagramcrawler.items import InstagramcrawlerItem
from instagramcrawler.spiders.seleniumscraper import InstagramCrawler

from selenium import webdriver

import json
import re


def load(filename):
    datastr = open(filename).read()
    data = json.loads(datastr)
    return data

class InstaSpider(BaseSpider):
    name = "instaspider"
    allowed_domains = ["instagram.com"]
    start_urls = [
                    "https://www.instagram.com/nishparadox",
            ]

    def __init__(self):
        super(InstaSpider, self).__init__() 
        self.data = load("./data/data.json")
        self.driver = webdriver.Firefox()
        self.instagram = InstagramCrawler(self.driver, self.data)
        self.instagram.run()

    """
    def init_request(self):
        request = FormRequest.from_response(
                    response,
                    formdata = self.data,
                    callback = self.logged_in,
                    meta = {'url_user' : "https://www.instagram.com/" + self.data['username'] + "/",
                        }
                )
        return Request(url=self.start_urls[0], callback=self.login)
    """

    def start_requests(self):
        print("-"*50, "inside start request")

        requests = [
                        Request(
                            url="https://www.instagram.com/{}".format(self.data['USERNAME']), 
                            callback=self.parse,
                            meta = { "type" : "owner" }
                        )

                ]

        requests += [
                        Request(
                            url="https://www.instagram.com/{}".format(username), 
                            callback=self.parse,
                            meta = { "type" : "follower" }
                        )

                        for username in self.instagram.followers
                ]

        requests += [
                        Request(
                            url="https://www.instagram.com/{}".format(username), 
                            callback=self.parse,
                            meta = { "type" : "following" }
                        )

                        for username in self.instagram.following
                ]
        return requests


    def clean_data(self, data):
        script_text = re.sub(r'<script type="text/javascript">window._sharedData = ', "", data)
        script_text = re.sub(r";</script>", "", script_text)
        script_text = script_text.strip()
        data = json.loads(script_text)
        return data['entry_data']['ProfilePage'][0]['user']

    def parse(self, response):
        item = InstagramcrawlerItem()
        print("-"*50, "inside parse")
        sel = Selector(response)
        script = response.xpath("//script")[-5]
        user = self.clean_data(script.extract())

        item['full_name'] = user['full_name']
        item['username'] = user['username']
        item['bio'] = user['biography'] if user['biography'] else ""
        item['followers'] = user['followed_by']['count']
        item['following'] = user['follows']['count']

        item['item_type'] = response.meta['type']

        yield item






