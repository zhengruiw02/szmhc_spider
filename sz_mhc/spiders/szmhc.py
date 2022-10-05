import scrapy

from scrapy.loader import ItemLoader
from sz_mhc.items import SzMhcItem

# for regex use
import re

class SzmhcSpider(scrapy.Spider):
    name = 'szmhc'
    allowed_domains = ['wjw.sz.gov.cn']
    
    def start_requests(self):
        url = 'http://wjw.sz.gov.cn/yqxx/index.html'


        yield scrapy.Request(url, callback=self.findInPage)

    def findInPage(self, response):
        
        xpath_href = '//a[contains(text(), "深圳市新冠肺炎疫情情况")]/@href'

        l = ItemLoader(item=SzMhcItem(), response=response)

        daily_report_urls = response.xpath(xpath_href).extract()
        if daily_report_urls is not None:
            for daily_report_url in daily_report_urls:
                #print(daily_report_url)
                yield scrapy.Request(daily_report_url, callback=self.parse)

        next_page_url = response.xpath('//a[contains(text(), "下一页")]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.findInPage)
        return l.load_item()


    def parse(self, response):

        parser = {
            'date' : r"(\d{1,2})月(\d{1,2})日",
            'fullDate' : r"(\d{1,2}月\d{1,2}日)",
            'cases' : r"新增[^0-9]*(\d{1,2})例[^0-9]*(\d{1,2})例",
        }

        report_para_innerCity = response.xpath('string(//p[@style][1])').extract_first()
        #report_para_enteringCountry = response.xpath('string(//p[@style][2])').extract_first()

        print(report_para_innerCity)
        #print(report_para_enteringCountry)

        results = {}
        # date
        # result = re.findall(parser['date'], report_para_innerCity)
        # if(result):
        #     print(result)
        #     if(result[0][0]):
        #         results['month'] = result[0][0]
        #     if(result[0][1]):
        #         results['day'] = result[0][1]
            
        #     print(results['month'], results['day'])
            
        # fullDate
        result = re.findall(parser['fullDate'], report_para_innerCity)
        if(result):
            print(result)
            if(result[0]):
                results['date'] = result[0]
            
            # print(results['date'])

        # cases
        result = re.findall(parser['cases'], report_para_innerCity)
        if(result):
            print(result)
            if(result[0][0]):
                results['confirmed'] = result[0][0]
            if(result[0][1]):
                results['asymptomatic'] = result[0][1]
            
            # print(results['confirmed'], results['asymptomatic'])

            
        l = ItemLoader(item=SzMhcItem(), response=response)

        l.add_value('date', results['date'])
        # l.add_value('month', results['month'])
        # l.add_value('day', results['day'])
        if(results['confirmed']):
            l.add_value('confirmed', results['confirmed'])
        if(results['asymptomatic']):
            l.add_value('asymptomatic', results['asymptomatic'])

        yield l.load_item()

    
