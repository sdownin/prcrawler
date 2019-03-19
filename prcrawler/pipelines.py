# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json, pymongo, logging
from prcrawler import settings
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline


class ImagesPipeline(ImagesPipeline):
    """ Pipelines order: 1
    """
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            logging.info("ImagesPipeline::get_media_requests:  yielding Request(image_url)")
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['image_paths'] = image_paths
            logging.info("ImagesPipeline::item_completed:  added pdf_paths to item")
            return item
        else:
            logging.info("Item contains no images")
            

class PdfsPipeline(FilesPipeline):
    """ Pipelines order: 10
    """
    def get_media_requests(self, item, info):
        for pdf_url in item['pdf_urls']:
            logging.info("PdfsPipeline::get_media_requests:  yielding Request(pdf_url)")
            yield Request(pdf_url)

    def item_completed(self, results, item, info):
        pdf_paths = [x['path'] for ok, x in results if ok]
        if pdf_paths:
            item['pdf_paths'] = pdf_paths
            logging.info("PdfsPipeline::item_completed:  get_media_requests: added pdf_paths to item")
            return item
        else:
            logging.info("Item contains no PDFs")


class MongoPipeline(object):
    """ Pipelines order: 100
    """
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = settings.MONGODB_COLLECTION

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid and (item['article'] is not None or not item['has_dom_article']):
            self.db[self.collection_name].insert_one(dict(item))
            logging.info("Item added to MongoDB!")
        return
    

class JsonWriterPipeline(object):
    """ Pipelines order: 200
    """
    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item


class PrcrawlerPipeline(object):

    def process_item(self, item, spider):
        return item