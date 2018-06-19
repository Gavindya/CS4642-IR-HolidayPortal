# https://www.airbnb.com/
import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
# from tutorial.spiders import AirBnBScraperItem


class LankaHolidaysSpider(CrawlSpider):

    name = "lankaholidays"
    allowed_domains = ['lankaholidays.com']
    # start_urls = [
    #     'http://www.lankaholidays.com/index.php?page=2&location=North+Central_Anuradhapura',
    # ]
    start_urls = ['http://www.lankaholidays.com/index.php?page=%s&location=North+Central_Anuradhapura'
                  % page for page in range(1, 11)]

    # This spider has one rule: extract all (unique and canonicalized) links,
    # follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_item",
        )
    ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        count = 0
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={'count': count})
            count = count + 1

    # Method for parsing items
    def parse(self, response):
        # The list of items that are found on the particular page
        items = []
        # Only extract canonicalized and unique links (with respect to the current page)
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        # Now go through all the found links
        for link in links:
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            # If it is allowed, create a new item and add it to the list of found items
            if is_allowed:
                item = link.url
                items.append(item)

        # Write items[] to csv
        filename = 'scraped_links/%s.txt' % response.request.meta['count']
        with open(filename, 'w') as f:
            for i in items:
                f.write(i)
                f.write('\n')

        # next_page = response.css('li.next a::attr("href")').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)

        # next_page = response.xpath("//a[@class='next_page']/@href").extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)


# scrapy crawl airbnb

# scrapy crawl airbnb -o airbnb_links.csv -t csv