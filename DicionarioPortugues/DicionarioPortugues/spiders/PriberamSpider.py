import scrapy
import constants

TEST_URL = 'https://dicionario.priberam.org/amar'

class InfopediaSpider(scrapy.Spider):
    name = "priberam"

    def start_requests(self):
        # urls = [
        #     'https://quotes.toscrape.com/page/1/',
        #     'https://quotes.toscrape.com/page/2/',
        # ]
        yield scrapy.Request(url=TEST_URL, callback=self.parse)


    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = f'html/{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
