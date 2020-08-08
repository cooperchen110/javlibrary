import scrapy
import string
import os
from myscrapy.items import ActorItem, VideoItem


class VideoRestSpider(scrapy.Spider):
    name = 'video_rest'
    allowed_domains = ['javlibrary.com']
    file_path = os.path.abspath('') + '/log/video_rest.txt'
    with open(file_path, 'r') as f:
        start_urls = [ i.strip() for i in f.readlines()]


    def parse(self, response):
        item = VideoItem()
        item['vid'] = response.xpath('//div[@id="video_id"]//td[@class="text"]/text()').extract_first()
        item['href'] = response.url
        item['title'] = response.xpath('//div[@id="video_title"]/h3/a/text()').extract_first()
        item['date'] = response.xpath('//div[@id="video_date"]//td[@class="text"]/text()').extract_first()
        item['length'] = response.xpath('//div[@id="video_length"]//span[@class="text"]/text()').extract_first()
        item['score'] = response.xpath('//div[@id="video_review"]//span[@class="score"]/text()').extract_first()
        item['genres'] = response.xpath('//div[@id="video_genres"]//span[@class="genre"]/a/text()').extract()
        item['casts'] = response.xpath('//div[@id="video_cast"]//span[@class="star"]/a/text()').extract()
        yield item




