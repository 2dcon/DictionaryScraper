import scrapy
import constants


class VerbSpider(scrapy.Spider):
    name = "verb"

    def start_requests(self):
        # urls = [
        url_verb = constants.URLVERB
        with open('WordList/verbs', 'r') as verbs:
            for word in verbs:
                url = url_verb + word.strip()
                yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = f'verbs/{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
