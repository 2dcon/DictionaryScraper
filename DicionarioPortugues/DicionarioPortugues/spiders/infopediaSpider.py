import logging
import os

import scrapy
from scrapy.utils.log import configure_logging

URLS = 'infopedia/urls'
CLASS_CONJ = 'conjugar'
ROOT_URL = 'https://www.infopedia.pt'

HTML_PATH = 'infopedia/html'
CONJ_PATH = 'infopedia/conj'

TEST_URL = 'https://www.infopedia.pt/dicionarios/lingua-portuguesa/uioashfioaushfoaisudf'

class InfopediaSpider(scrapy.Spider):
    name = "infopedia"
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='infopedia.log',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def start_requests(self):
        if not os.path.exists(HTML_PATH):
            os.makedirs(HTML_PATH)

        if not os.path.exists(CONJ_PATH):
            os.makedirs(CONJ_PATH)

        with open(URLS, 'r') as file:
            urls = file.readlines()
            total = len(urls)

            for i in range(total):
                yield scrapy.Request(url=urls[i], callback=self.parse)
                print('\r', f'progress: {i}/{total}', end='')

        # yield scrapy.Request(url=TEST_URL, callback=self.parse)

    def parse(self, response):
        div_entry = response.xpath("//div[@class='dolEntradaVverbete']")
        div_inflection = response.xpath("//div[@class='QuadroAnamorfs QuadroAnamorfsTop']")

        if div_entry and not div_inflection:
            page = response.url.split("/")[-1]
            filename = f'{HTML_PATH}/{page}'
            with open(filename, 'wb') as f:
                f.write(response.body)

            conj = response.xpath("//p[@class='conjugar']/a/@href").get()

            if conj:
                url_conj = ROOT_URL + conj
                yield scrapy.Request(url=url_conj, callback=self.get_conj)

            self.log(f'Saved file {filename}')

    def get_conj(self, response):
        page = response.url.split("/")[-1]
        filename = f'{CONJ_PATH}/{page}'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')