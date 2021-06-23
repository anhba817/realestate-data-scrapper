import scrapy
from datetime import datetime

class WilliamsonSpider(scrapy.Spider):
    name = 'sterlingmgmt'
    PAGE_MAX = 4

    def start_requests(self):
        urls = [
            'http://www.sterlingmgmt.ca/residential/Multiplex/Fort%20St%20John//all',
            'http://www.sterlingmgmt.ca/residential/House/Fort%20St%20John//all',
        ]
        self.date = datetime.now()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.css('.imagecache-linked::attr(href)'):
            yield response.follow(href, callback=self.parse_article)
    
    def parse_article(self, response):
        values = response.css('div.field.field-res-building-type').xpath('.//div/div/text()').getall()
        building_type = values[-1].strip() if values else ''
        values = response.css('div.field.field-prop-avail').xpath('.//div/div/text()').getall()
        availability = values[-1].strip() if values else ''
        values = response.css('div.field.field-res-rent').xpath('.//div/div/text()').getall()
        rent = values[-1].strip().split('.')[0] if values else ''
        values = response.css('div.field.field-res-deposit').xpath('.//div/div/text()').getall()
        security_deposit = values[-1].strip() if values else ''
        values = response.css('div.field.field-res-bedrooms').xpath('.//div/div/text()').getall()
        bedrooms = values[-1].strip() if values else ''
        values = response.css('div.field.field-res-bathrooms').xpath('.//div/div/text()').getall()
        bathrooms = values[-1].strip() if values else ''
        values = response.css('div.field.field-res-units').xpath('.//div/div/text()').getall()
        units_in_building = values[-1].strip() if values else ''
        yield {
            'date': self.date.strftime("%m/%d/%Y"),
            'building_type': building_type,
            'availability': availability,
            'rent': rent,
            'security_deposit': security_deposit,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'units_in_building': units_in_building,
            'address': response.css('div.field.field-prop-full-address').xpath('.//div/div/text()').get(default='').strip(),
        }
