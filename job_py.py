import scrapy
import datetime


class JobPySpider(scrapy.Spider):
    name = 'job.py'
    allowed_domains = ['ycombinator.com']
    start_urls = ['https://news.ycombinator.com/jobs']

    def parse(self, response):
        count = -1
        for job in response.css('tr.athing'):
            count += 1

            k = response.css('td.subtext')[count]
            data = k.css('span.age > a::text').extract_first()

            if data[0] == '6':
                break

            if data[2:5] == 'day':
                today = datetime.date.today()
                check = int(data[0])
                get_date = today - datetime.timedelta(days=check)
                get_date = f'{get_date.day}-{get_date.month}-{get_date.year}'
            else:
                get_date = datetime.date.today()
                get_date = f'{get_date.day}-{get_date.month}-{get_date.year}'

            item = {
                'Job_Title': job.css('a.storylink::text').extract_first(),
                'Company_URL': job.css('span.sitestr::text').extract_first(),
                'Job_URL': job.css('tr.athing > td > a::attr(href)').extract_first(),
                'Job_Posting_date': get_date
            }

            yield item
