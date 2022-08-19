import string

import scrapy
from scrapy import Selector

ROOT_URL = 'https://dizionari.repubblica.it/Italiano/'
WORD_URL = 'https://dizionario.internazionale.it/parola/'
TEST_URL = 'https://dizionari.corriere.it/dizionario_italiano/a.shtml'
URL_FILE = 'repubblica/urls'
FAILED_LOG = 'repubblica/failed'


class MauroSpider(scrapy.Spider):
    name = "repubblica"

    def start_requests(self):
        # yield scrapy.Request(url=TEST_URL, callback=self.test)
        for letter in string.ascii_lowercase:
            letter_url = ROOT_URL + letter + '.html'
            # get page number
            yield scrapy.Request(url=letter_url, meta={'letter': letter, 'page': 1}, callback=self.get_page_range)

    def get_page_range(self, response):
        if response.status == 404:
            with open(FAILED_LOG, 'a') as f:
                f.write('404: ' + response.url + '\n')
        else:
            sel = Selector(response)

            wordlist = sel.xpath("//div[@class='descrizione']/ul/a/@href").extract()
            if len(wordlist):
                with open(URL_FILE, 'a') as f:
                    for word in wordlist:
                        url = ROOT_URL + word + '\n'
                        f.write(url)

                next_page = sel.xpath("//a[contains(., 'Avanti ')]/@href").get()
                # keeps requesting until nothing is in the page
                if next_page:
                    next_page = ROOT_URL + next_page
                    yield scrapy.Request(url=next_page, callback=self.get_page_range)
            else:
                with open(FAILED_LOG, 'a') as f:
                    f.write('empty: ' + response.url + '\n')
