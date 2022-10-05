# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
from scrapy.exporters import CsvItemExporter
import json


class SzMhcPipeline:    
    file = None
    
    def open_spider(self, spider):
        self.file = open('Shenzhen_COVID19_results.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, include_headers_line=True, join_multivalued=',', encoding='utf-8-sig')
        self.exporter.start_exporting()
        
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
