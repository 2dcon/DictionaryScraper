import os.path

from scrapy.spiders import SitemapSpider

PATH = 'lexico/html'


class LexicoSpider(SitemapSpider):
    name = 'lexico'

    sitemap_urls = ['https://www.lexico.pt/sitemap.xml']

    def __init__(self):
        super(LexicoSpider, self).__init__()

        if not os.path.exists(PATH):
            os.makedirs(PATH)

    def parse(self, response):
        title = response.xpath("//h1[@class='title']/text()").get()
        main_content = response.xpath("//div[@class='main-content']").get()

        if title and main_content:
            html = f'{PATH}/{title}.html'
            with open(html, 'w') as f:
                f.write(main_content)
