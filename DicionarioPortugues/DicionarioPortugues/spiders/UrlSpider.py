# scrapy crawl url -a path=/path/with/url/list
import logging
import os.path
import scrapy
from scrapy.utils.log import configure_logging


class UrlSpider(scrapy.Spider):
    name = "url"
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def __init__(self, path=None, *args, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.failed = []

    def start_requests(self):
        url_path = self.path + '/urls'
        html_path = self.path + '/html'

        if not os.path.exists(html_path):
            os.makedirs(html_path)

        with open(url_path, 'r') as file:
            urls = file.readlines()
            total = len(urls)
            for i in range(len(urls)):
                yield scrapy.Request(url=urls[i], meta={'html_path': html_path}, callback=self.parse)
                print('\r', f'progress: {i}/{len(urls)}', end='')

    def parse(self, response):
        page = response.url.split("/")[-1]
        path = response.meta.get('html_path')

        filename = f'{path}/{page}'

        with open(filename, 'wb') as f:
            f.write(response.body)
