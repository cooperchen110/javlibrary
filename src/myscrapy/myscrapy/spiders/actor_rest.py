import scrapy
import string
import os
from myscrapy.items import ActorItem, VideoItem


class ActorRestSpider(scrapy.Spider):
    name = 'actor_rest'
    allowed_domains = ['javlibrary.com']
    file_path = os.path.abspath('') + '/log/actor_rest.txt'
    with open(file_path, 'r') as f:
        start_urls = [ i.strip() for i in f.readlines()]
    base_url = 'http://www.javlibrary.com'

    def parse(self, response):
        div_list = response.xpath('//div[@class="video"]')
        for div in div_list:
            item = VideoItem()
            item['vid'] = div.xpath('.//div[@class="id"]/text()').extract_first()
            href = div.xpath('./a/@href').extract_first()
            item['href'] = self.base_url + '/cn/' + href.split('./')[-1]
            yield scrapy.Request(item['href'], callback=self.parse_video, meta={'item': item}, dont_filter = False)
        next_url = response.xpath('//a[@class="page next"]/@href').extract_first()
        if next_url is not None:
            next_url = self.base_url + next_url
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_video(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//div[@id="video_title"]/h3/a/text()').extract_first()
        item['date'] = response.xpath('//div[@id="video_date"]//td[@class="text"]/text()').extract_first()
        item['length'] = response.xpath('//div[@id="video_length"]//span[@class="text"]/text()').extract_first()
        item['score'] = response.xpath('//div[@id="video_review"]//span[@class="score"]/text()').extract_first()
        item['genres'] = response.xpath('//div[@id="video_genres"]//span[@class="genre"]/a/text()').extract()
        item['casts'] = response.xpath('//div[@id="video_cast"]//span[@class="star"]/a/text()').extract()
        yield item




