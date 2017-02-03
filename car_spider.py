import scrapy
from scrapy.linkextractors import LinkExtractor

class NewCarSpider(scrapy.Spider):
    name = "tw-new-car"
    start_urls = [
        'https://tw.autos.yahoo.com/car-research/',
    ]

    def parse(self, response):
        for car_maker in LinkExtractor(restrict_css='.make-list').extract_links(response):
            yield scrapy.Request(car_maker.url, callback=self.parse_maker)

    def parse_maker(self, response):
        for car_model in LinkExtractor(restrict_css='.model-list').extract_links(response):
            yield scrapy.Request(car_model.url, callback=self.parse_model)

    def parse_model(self, response):
        for model_trim in LinkExtractor(restrict_css='.model').extract_links(response):
            yield scrapy.Request(model_trim.url, callback=self.parse_trim)

    def parse_trim(self, response):
        pass
