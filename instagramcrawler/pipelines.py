# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class InstagramcrawlerPipeline(object):
    def __init__(self):
        self.owner = {}
        self.followers_data = []
        self.following_data= []
        self.filename = "./data/dump.json"

    def process_item(self, item, spider):
        print("-" * 50)
        data = dict(item)
        # pipeline the item accordingly
        if item['item_type'] == "owner":
            del data['item_type']
            self.owner = data

        elif item['item_type'] == "follower":
            del data['item_type']
            self.followers_data.append(data)
        else:
            del data['item_type']
            self.following_data.append(data)
        return data

    # when spider closes, dump the data to json
    def close_spider(self, spider):
        print("-" * 50)
        print("inside close_spider()")
        data = self.owner
        data['followers'] = self.followers_data
        data['following'] = self.following_data
        self.dump(self.filename, data)

    def dump(self, filename, data):
        configstr = json.dumps(data, indent=4)
        with open(filename, "w") as outfile:
            outfile.write(configstr)

