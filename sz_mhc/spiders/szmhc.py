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
            'noIncrease' : r"无本土", #http://wjw.sz.gov.cn/yqxx/content/post_9730245.html
            'singleCase' : r"([男女])，(\d*?)岁，居住在(.*?区)(.*?街道)(.*?)，在(.*?)中发现。",
        }

        report_para_full = response.xpath('string(//div[@class="news_cont_d_wrap"])').extract_first()
        # print(report_para_full)

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
                print(results['date'])

        # cases
        result = re.findall(parser['cases'], report_para_innerCity)
        if(result):
            print(result)
            if(result[0][0]):
                results['confirmed'] = result[0][0]
            if(result[0][1]):
                results['asymptomatic'] = result[0][1]
            
            # print(results['confirmed'], results['asymptomatic'])

        # single case
        result = re.findall(parser['singleCase'], report_para_full)
        if(result):
            # print(results)
            results['casesList'] = {}
            results['casesSum'] = {}
            results['casesSum']['sexual'] = {}
            results['casesSum']['age'] = {}
            results['casesSum']['district'] = {}
            results['casesSum']['subDistrict'] = {}
            results['casesSum']['caseDivision'] = {}
            i = 0
            for eachResult in result:
                # print(eachResult)
                results['casesList'][i] = {}
                if(eachResult[0]):
                    caseSexual = eachResult[0]
                    results['casesList'][i]['sexual'] = caseSexual
                    if caseSexual in results['casesSum']['sexual']:
                        results['casesSum']['sexual'][caseSexual] += 1
                    else:
                        results['casesSum']['sexual'][caseSexual] = 1
                if(eachResult[1]):
                    caseAge = int(eachResult[1])
                    results['casesList'][i]['age'] = caseAge
                    if(caseAge < 10):
                        if "0-9" in results['casesSum']['age']:
                            results['casesSum']['age']["0-9"] += 1
                        else:
                            results['casesSum']['age']["0-9"] = 1
                    elif(caseAge < 20):
                        if "10-19" in results['casesSum']['age']:
                            results['casesSum']['age']["10-19"] += 1
                        else:
                            results['casesSum']['age']["10-19"] = 1
                    elif(caseAge < 30):
                        if "20-29" in results['casesSum']['age']:
                            results['casesSum']['age']["20-29"] += 1
                        else:
                            results['casesSum']['age']["20-29"] = 1
                    elif(caseAge < 40):
                        if "30-39" in results['casesSum']['age']:
                            results['casesSum']['age']["30-39"] += 1
                        else:
                            results['casesSum']['age']["30-39"] = 1
                    elif(caseAge < 50):
                        if "40-49" in results['casesSum']['age']:
                            results['casesSum']['age']["40-49"] += 1
                        else:
                            results['casesSum']['age']["40-49"] = 1
                    elif(caseAge < 60):
                        if "50-59" in results['casesSum']['age']:
                            results['casesSum']['age']["50-59"] += 1
                        else:
                            results['casesSum']['age']["50-59"] = 1
                    elif(caseAge < 70):
                        if "60-69" in results['casesSum']['age']:
                            results['casesSum']['age']["60-69"] += 1
                        else:
                            results['casesSum']['age']["60-69"] = 1
                    elif(caseAge < 80):
                        if "70-79" in results['casesSum']['age']:
                            results['casesSum']['age']["70-79"] += 1
                        else:
                            results['casesSum']['age']["70-79"] = 1
                    elif(caseAge < 90):
                        if "80-89" in results['casesSum']['age']:
                            results['casesSum']['age']["80-89"] += 1
                        else:
                            results['casesSum']['age']["80-89"] = 1
                    else:
                        if "90+" in results['casesSum']['age']:
                            results['casesSum']['age']["90+"] += 1
                        else:
                            results['casesSum']['age']["90+"] = 1
                if(eachResult[2]):
                    caseDistrict = eachResult[2]
                    results['casesList'][i]['district'] = caseDistrict
                    if caseDistrict in results['casesSum']['district']:
                        results['casesSum']['district'][caseDistrict] += 1
                    else:
                        results['casesSum']['district'][caseDistrict] = 1
                if(eachResult[3]):
                    caseSubDistrict = eachResult[3]
                    results['casesList'][i]['subDistrict'] = caseSubDistrict
                    if caseSubDistrict in results['casesSum']['subDistrict']:
                        results['casesSum']['subDistrict'][caseSubDistrict] += 1
                    else:
                        results['casesSum']['subDistrict'][caseSubDistrict] = 1
                if(eachResult[4]):
                    caseAddress = eachResult[4]
                    results['casesList'][i]['address'] = caseAddress
                if(eachResult[5]):
                    caseDivision = eachResult[5]
                    results['casesList'][i]['caseDivision'] = caseDivision
                    if caseDivision in results['casesSum']['caseDivision']:
                        results['casesSum']['caseDivision'][caseDivision] += 1
                    else:
                        results['casesSum']['caseDivision'][caseDivision] = 1
                i += 1

        print(results)
            
        l = ItemLoader(item=SzMhcItem(), response=response)

        l.add_value('date', results['date'])
        # l.add_value('month', results['month'])
        # l.add_value('day', results['day'])
        if(results['confirmed']):
            l.add_value('confirmed', results['confirmed'])
        if(results['asymptomatic']):
            l.add_value('asymptomatic', results['asymptomatic'])

        yield l.load_item()

    
