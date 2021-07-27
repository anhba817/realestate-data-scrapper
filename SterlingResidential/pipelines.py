# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from exporters import MyCsvItemExporter

class CsvExportPipeline:
    def open_spider(self, spider):
        self.csv_file = open('results.csv', 'wb')
        self.exporter = MyCsvItemExporter(
            self.csv_file,
            fields_to_export=['source', 'date', 'title', 'building_type', 'availability', 'rent', 'security_deposit', 'utilities', 'bedrooms', 'bathrooms', 'units_in_building', 'address'],
        )
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csv_file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class DuplicatesPipeline:
    def __init__(self):
        self.articles_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['title'] in self.articles_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.articles_seen.add(adapter['title'])
            return item

class FilterCityPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "Fort St. John" not in adapter['city']:
            raise DropItem(f"Wrong city: {item!r}")
        elif adapter['utilities'].lower() != "not included":
            raise DropItem(f"Utilities is not Not Included: {item!r}")
        else:
            return item