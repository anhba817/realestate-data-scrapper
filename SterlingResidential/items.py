# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SterlingresidentialItem(scrapy.Item):
    # define the fields for your item here like:
    source = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    building_type = scrapy.Field()
    availability = scrapy.Field()
    city = scrapy.Field()
    rent = scrapy.Field()
    security_deposit = scrapy.Field()
    utilities = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    units_in_building = scrapy.Field()
    address = scrapy.Field()
