import os.path

from scrapy.spiders import SitemapSpider

PATH = 'chitanka/html'


class ChitankaSpider(SitemapSpider):
    name = 'chitanka'

    sitemap_urls = ['http://rechnik.chitanka.info/sitemap.xml']

    def __init__(self):
        super(ChitankaSpider, self).__init__()

        if not os.path.exists(PATH):
            os.makedirs(PATH)

    def parse(self, response):
        if response is not None:
            title = response.xpath("//h1[@id='first-heading']/text()").get()
            main_content = response.xpath("//div[@class='box']").get()

            if title and main_content:
                html = f'{PATH}/{title}.html'
                with open(html, 'w') as f:
                    f.write(main_content)
