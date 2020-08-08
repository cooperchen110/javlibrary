# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ActorItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    href = scrapy.Field()
    aid = scrapy.Field()

class VideoItem(scrapy.Item):
    vid = scrapy.Field()
    actor = scrapy.Field()
    aid = scrapy.Field()
    href = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    length = scrapy.Field()
    score = scrapy.Field()
    genres = scrapy.Field()
    casts = scrapy.Field()
