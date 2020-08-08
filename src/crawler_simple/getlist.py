import requests
import sys
import string
import json
import random
import logging
import time
from lxml import etree
from fake_useragent import UserAgent
from openpyxl import Workbook
from threading import Thread
from retry import retry

logging.basicConfig(level=logging.INFO)

class Javlibrary:
    def __init__(self):
        self.html_code = 1
        self.actor_list_url = 'http://www.javlibrary.com/cn/star_list.php?prefix={}&page={}'
        self.base_url = 'http://www.javlibrary.com/cn/'
        self.actor_url = 'http://www.javlibrary.com/cn/vl_star.php?s={}&page={}'
        self.proxypool_apikey = 'ec71b195426668bf89ce7a1f5d2208f94fe4e64d'
        self.excel_filename = './data.xlsx'
        self.proxy_filename = './proxy.txt'
        self.alphabet = list(string.ascii_uppercase)
        self.proxypool_page_max = 4
        self.proxypool_url = 'https://proxy.webshare.io/api/proxy/list/?page={}'
        self.useragent = UserAgent(verify_ssl=False)
        self.proxypool = []
        self.wb = Workbook()
        self.ws1 = self.wb.active
        self.ws1.title = 'actors'
        self.ws2 = self.wb.create_sheet(title='videos')
        self.ws1_header = ['id', 'name']
        self.ws1.append(self.ws1_header)
        self.ws2_header = ['vid', 'title', 'date', 'length',  'score', 'genres', 'casts']
        self.ws2.append(self.ws2_header)


    def proxypool_update(self):
        self.initalize_proxypool()
        time.sleep(3000)
        self.proxypool = [p for p in self.proxypool if self.check_proxy(p)]
        logging.info(f'totally {len(self.proxypool)} valid proxies in the pool')


    def initalize_proxypool(self):
        self.proxypool = []
        for i in range(1, self.proxypool_page_max+1):
            url = self.proxypool_url.format(i)
            res = requests.get(url, headers={"Authorization": f"Token {self.proxypool_apikey}"})
            dic = res.json()
            self.proxypool.extend(dic['results'])
            logging.info(f'added {len(dic["results"])} proxies to proxypool, totally {len(self.proxypool)} proxies in the pool')


    def check_proxy(self, proxy):
        proxies = {
            'http': f'http://{proxy["username"]}:{proxy["password"]}@{proxy["proxy_address"]}:{proxy["ports"]["http"]}/',
            'https': f'http://{proxy["username"]}:{proxy["password"]}@{proxy["proxy_address"]}:{proxy["ports"]["http"]}/',
        }
        headers = {'user-agent': self.useragent.random}
        try:
            res = requests.get(self.base_url, headers=headers, proxies=proxies)
            logging.info(f'proxy \t {proxy["proxy_address"]} \t ==> status code \t {res.status_code}')
            if res.status_code == 200:
                return True
            else:
                return False
        except:
            return False


    @retry(tries=3)
    def get_html(self, url):
        headers = {'user-agent': self.useragent.random}
        proxy = random.choice(self.proxypool)
        proxies = {
            'http': f'http://{proxy["username"]}:{proxy["password"]}@{proxy["proxy_address"]}:{proxy["ports"]["http"]}/',
            'https': f'http://{proxy["username"]}:{proxy["password"]}@{proxy["proxy_address"]}:{proxy["ports"]["http"]}/',
        }
        res = requests.get(url, headers=headers, proxies=proxies)
        html_str = res.content.decode()
        with open(f'./html/{self.html_code}.html', 'w') as f:
            f.write(html_str)
            logging.info(f'html code {self.html_code} write successfully')
            self.html_code += 1
        html = etree.HTML(html_str)
        return html


    def get_xpath(self, root, xpath):
        return root.xpath(xpath)[0] if root.xpath(xpath) else None


    def get_page(self):
        print('executing get_page')
        page_num_list = []
        for letter in self.alphabet:
            entry = {}
            entry['letter'] = letter
            url = self.actor_list_url.format(letter, 1)
            html = self.get_html(url)
            last_page_url = self.get_xpath(html, '//a[@class="page last"]/@href')
            entry['page_num'] = int(last_page_url.split('page=')[-1])
            for page in range(1, entry['page_num']+1):
                logging.info(f'executing ==> preffix \t {letter} \t page \t {page}')
                self.get_actor_list(letter, page)
        sys.exit('finished')


    def get_actor_list(self, letter, page):
        print('executing get_actor_list')
        url = self.actor_list_url.format(letter, page)
        html = self.get_html(url)
        item_list = html.xpath('//div[@class="searchitem"]')
        for item in item_list:
            actor = {}
            actor['id'] = self.get_xpath(item, './@id')
            actor['name'] = self.get_xpath(item, './a/text()')
            row = [actor[i] for i in self.ws1_header]
            self.ws1.append(row)
            logging.info(f'id-{actor["id"]} wrote successfully')
            self.get_all_video_list(actor['id'])
        self.wb.save(self.excel_filename)


    def get_video_list(self, url):
        print('executing get_video_list')
        html = self.get_html(url)
        last_page = self.get_xpath(html, '//a[@class="page last"]/@href')
        item_list = html.xpath('//div[@class="video"]')
        video_list = []
        for item in item_list:
            video = {}
            video['vid'] = self.get_xpath(item, './/div[@class="id"]/text()')
            short_url = self.get_xpath(item,'./a/@href')
            video['url'] = self.base_url + short_url.split('./')[-1]
            dic = self.get_video_info(video['url'])
            video = {**video, **dic}
            row = [str(video[i]) for i in self.ws2_header]
            self.ws2.append(row)
            logging.info(f'vid-{video["vid"]} wrote successfully')
            video_list.append(video)
        self.wb.save(self.excel_filename)
        logging.info('excel saved successfully')
        return last_page


    def get_all_video_list(self, actor_id):
        first_url = self.actor_url.format(actor_id, 1)
        last_page = self.get_video_list(first_url)
        print('****** last page', last_page)
        if last_page:
            page_num = int(last_page.split('page=')[-1])
            for page in range(2, page_num+1):
                other_url = self.actor_url.format(actor_id, page)
                other_last_page = self.get_video_list(other_url)


    def get_video_info(self, video_url):
        video = {}
        html = self.get_html(video_url)
        video['title'] = self.get_xpath(html, '//div[@id="video_title"]/h3/a/text()')
        video['date'] = self.get_xpath(html, '//div[@id="video_date"]//td[@class="text"]/text()')
        video['length'] = self.get_xpath(html, '//div[@id="video_length"]//span[@class="text"]/text()')
        video['score'] = self.get_xpath(html, '//div[@id="video_review"]//span[@class="score"]/text()')
        video['genres'] = html.xpath('//div[@id="video_genres"]//span[@class="genre"]/a/text()')
        video['casts'] = html.xpath('//div[@id="video_cast"]//span[@class="star"]/a/text()')
        return video


    def run(self):
        self.initalize_proxypool()
        self.get_page()

        # t1 = Thread(target=self.proxypool_update())
        # t1.start()
        # time.sleep(10)
        # t2 = Thread(target=self.get_page())
        # t2.start()


if __name__ == '__main__':
    javlibrary = Javlibrary()
    javlibrary.run()
