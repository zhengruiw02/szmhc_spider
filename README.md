# Shenzhen COVID-19 Daily Information Spider

This is a scrapy spider to crawl Shenzhen COVID-19 daily information from [Shenzhen Municipal Health Commision website](http://wjw.sz.gov.cn/yqxx/index.html)

## Prerequest

* Python 3.9 or above
* Scrapy 2.6 or above

## Usage

locate to project folder, then use following command

```shell
scrapy crawl szmhc
```

After spider done, you will get output file named `'Shenzhen_COVID19_results.csv'`
