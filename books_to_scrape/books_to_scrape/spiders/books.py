import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='http://books.toscrape.com/', headers={'User-Agent': self.user_agent})

    rules = (
        # For searching book links
        Rule(LinkExtractor(restrict_xpaths='//article[@class = "product_pod"]/h3/a'), callback='parse_item',
             follow=True, process_request='set_user_agent'),
        # For next page
        Rule(LinkExtractor(restrict_xpaths='//li[@class = "next"]/a'),
             process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath('//p[@class = "price_color"]/preceding-sibling::h1/text()').get(),
            'genre': response.xpath('//ul[@class = "breadcrumb"]/li[3]/a/text()').get(),
            'price': response.xpath('//p[@class = "price_color"]/text()').get(),
            # Get rid of unnecesary spaces with normalize-space()
            'availability': response.xpath('normalize-space(//p[@class = "instock availability"]/i/following-sibling::text())').get(),
            # Relative urls (it completes with the main one) need the following function to become absolute
            'portrait_url': response.urljoin(response.xpath('//div[@class = "item active"]/img/@src').get()),
            'description': response.xpath('//div[@id = "product_description"]/following-sibling::p/text()').get()
        }
