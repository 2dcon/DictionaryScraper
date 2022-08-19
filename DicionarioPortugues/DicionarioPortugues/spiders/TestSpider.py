import scrapy


class TestSpider(scrapy.Spider):
    name = "test"

    def __init__(self, path=None, *args, **kwargs):
        super().__init__(**kwargs)
        self.path = path

    def start_requests(self):
        url = 'https://www.merriam-webster.com/dictionary/forward'
        yield scrapy.Request(url=url, callback=self.test)

    def test(self, response):
        file_path = self.path + '/test'
        with open(file_path, 'w') as file:
            file.write('test spider!')
