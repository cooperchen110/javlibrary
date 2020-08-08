# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from myscrapy.items import ActorItem, VideoItem
import pymongo


myclient = pymongo.MongoClient('mongodb://localhost:27017')

actordb = myclient['javlibrary']['actor']
videodb = myclient['javlibrary']['video']


class MyscrapyPipeline:
    def process_item(self, item, spider):
        if isinstance(item, ActorItem):
            actordb.insert(dict(item))
            print('actor===>', item['name'])
        elif isinstance(item, VideoItem):
            videodb.insert(dict(item))
            print('video===>', item['vid'])
        return item
