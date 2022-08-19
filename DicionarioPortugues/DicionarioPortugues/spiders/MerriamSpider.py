import logging
import string
import scrapy
from scrapy import Selector

BROWSE_URL = 'https://www.merriam-webster.com/browse/dictionary'
DICT_URL = 'https://www.merriam-webster.com/dictionary/'
TEST_URL = 'https://www.merriam-webster.com/browse/dictionary/a'


class MerriamSpider(scrapy.Spider):
    name = "merriam"

    def start_requests(self):

        for letter in string.ascii_lowercase:
            letter_url = BROWSE_URL + letter
            # get page number
            yield scrapy.Request(url=letter_url, meta={'letter_url': letter_url}, callback=self.get_page_limit)


    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = f'Merriam/{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

    def get_page_limit(self, response):
        sel = Selector(response)

        extracted = sel.xpath("//span[@class='counters']/text()").extract()
        if len(extracted):
            last_page = int(extracted[0].split()[-1])
            for i in range(1, last_page + 1):
                url = response.meta.get('letter_url') + f'/{i}'
                yield scrapy.Request(url=url, callback=self.get_word_links)

    def get_word_links(self, response):
        sel = Selector(response)

        with open('Merriam/urls_raw', 'a') as url_file:
            for url in sel.xpath("//a[@class='pb-4 pr-4 d-block']/@href").extract():
                word_link = f'{DICT_URL}{url}\n'
                url_file.write(word_link)
                # yield scrapy.Request(url=word_link, callback=self.parse)
