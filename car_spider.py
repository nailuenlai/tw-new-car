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
        #response.xpath("//div[@id='trim-info-spec']").xpath('.//table/tbody/tr').xpath('.//td/text()').extract()
        spec_kv, spec_list = response.xpath("//div[@id='trim-info-spec']/div/div")
        ret = {
            'model': response.css('.title').xpath('.//text()').extract_first(),
            'price': response.css('.price-num').xpath('.//strong/text()').extract_first(),
            'spec': dict([x.xpath('.//td/text()').extract() for x in spec_kv.xpath('.//table/tbody/tr')]),
            'equip': spec_list.xpath('.//table/tbody/tr').xpath('.//td/text()').extract(),
        }
        return ret
