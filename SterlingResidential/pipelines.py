# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sys 
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from exporters import MyCsvItemExporter

class CsvExportPipeline:
    def open_spider(self, spider):
        self.csv_file = open('results.csv', 'wb')
        self.exporter = MyCsvItemExporter(
            self.csv_file,
            fields_to_export=['date', 'building_type', 'availability', 'rent', 'security_deposit', 'bedrooms', 'bathrooms', 'units_in_building', 'address'],
        )
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csv_file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item