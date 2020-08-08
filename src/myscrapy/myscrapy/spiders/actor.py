import scrapy
import string
from myscrapy.items import ActorItem, VideoItem


class ActorSpider(scrapy.Spider):
    name = 'actor'
    allowed_domains = ['javlibrary.com']
    start_urls = ['http://www.javlibrary.com/cn/star_list.php?prefix=I']
    base_url = 'http://www.javlibrary.com'
    page_url = 'http://www.javlibrary.com/cn/star_list.php?prefix={}'
    alphabet = list(string.ascii_uppercase)

    def parse(self, response):
        div_list = response.xpath('//div[@class="searchitem"]')
        for div in div_list:
            item = ActorItem()
            href = div.xpath('./a/@href').extract_first()
            item['href'] = self.base_url + '/cn/'+ href
            yield item
            yield scrapy.Request(item['href'], callback=self.parse_actor, meta={'item': item})
        next_url = response.xpath('//a[@class="page next"]/@href').extract_first()
        print('next_url(page): ', next_url)
        if next_url is None:
            letter_now = response.url.split('prefix=')[-1][0]
            print('letter_now = ', letter_now)
            if letter_now != self.alphabet[-1]:
                letter_next = self.alphabet[self.alphabet.index(letter_now)+1]
                next_url = self.page_url.format(letter_next)
                print('next_letter_url', next_url)
                yield scrapy.Request(next_url, callback=self.parse)
        else:
            next_url = self.base_url + next_url
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_actor(self, response):
        div_list = response.xpath('//div[@class="video"]')
        for div in div_list:
            item = VideoItem()
            item['vid'] = div.xpath('.//div[@class="id"]/text()').extract_first()
            item['actor'] = response.meta['item']['name']
            item['aid'] = response.meta['item']['aid']
            href = div.xpath('./a/@href').extract_first()
            item['href'] = self.base_url + '/cn/' + href.split('./')[-1]
            yield scrapy.Request(item['href'], callback=self.parse_video, meta={'item': item}, dont_filter = False)
        next_url = response.xpath('//a[@class="page next"]/@href').extract_first()
        if next_url is not None:
            next_url = self.base_url + next_url
            yield scrapy.Request(next_url, callback=self.parse_actor)

    def parse_video(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//div[@id="video_title"]/h3/a/text()').extract_first()
        item['date'] = response.xpath('//div[@id="video_date"]//td[@class="text"]/text()').extract_first()
        item['length'] = response.xpath('//div[@id="video_length"]//span[@class="text"]/text()').extract_first()
        item['score'] = response.xpath('//div[@id="video_review"]//span[@class="score"]/text()').extract_first()
        item['genres'] = response.xpath('//div[@id="video_genres"]//span[@class="genre"]/a/text()').extract()
        item['casts'] = response.xpath('//div[@id="video_cast"]//span[@class="star"]/a/text()').extract()
        yield item




