# https://www.airbnb.com/
import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
import re
import fileinput

class LankaholidaysSpider(CrawlSpider):
    name = "lankaholidays_one_page"
    allowed_domains = ['lankaholidays.com/']
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse",
        )
    ]

    def start_requests(self):
        urls = []
        p = re.compile(r"http://www.lankaholidays.com/holiday-homes/accommodation_details-(\d+)\.html")
        # range - 0-10
        for item in range(0, 10):
            file = 'scraped_links/%s.txt' % item
            with open(file, 'r') as f:
                for line in f:
                    if p.match(line.strip()):
                        # print(line.strip())
                        urls.append(line.strip())

        for url in urls:
            # get the xxxx number in url to create the xxxx.html once scraped
            numbers = re.findall(r'\d+', url)
            # send xxxx number to the parse
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={'file_number': numbers[0]})

    # Method for parsing items
    def parse(self, response):
        # page = response.url.split("/")[-2]
        filename = 'scraped_html/%s.html' % response.request.meta['file_number']
        with open(filename, 'w') as fw:
            fw.write(response.body.decode("utf-8"))

        # these functions do not let me inspect. therefore removed them
        ns = re.compile(r"document.onmousedown=clickNS4;")
        ie = re.compile(r"document.onmousedown=clickIE4;")
        on = re.compile(r"document.oncontextmenu=new Function")

        # print('open\n')
        with fileinput.FileInput(filename, inplace=True, backup='.txt') as file:
            # print('open file')
            for line in file:
                # print('%s' % line.strip())
                if ns.match(line.strip()):
                    print(line.replace((line.strip()), '//document.onmousedown=clickNS4;'), end='')
                elif ie.match(line.strip()):
                    # print(line.strip())
                    print(line.replace((line.strip()), '//document.onmousedown=clickIE4;'), end='')
                elif on.match(line.strip()):
                    # print(line.strip())
                    print(line.replace((line.strip()), ''), end='')
                else:
                    print(line.strip())
