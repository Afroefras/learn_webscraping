import scrapy
from scrapy_splash import SplashRequest

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com/js',
                             callback=self.parse,
                             headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'},
                             endpoint="execute", 
                             args={'lua_source':self.script})

    def parse(self, response):
        for quote in response.xpath('//div[@class = "quote"]'):
            yield {
                'quote': quote.xpath('.//span[@class="text"]/text()').get(),
                'author': quote.xpath('.//span[2]/small[@class="author"]/text()').get(),
                'tags': quote.xpath('.//div[@class="tags"]/a/text()').getall()
            }

        next_page = response.xpath('//li[@class = "next"]/a/@href').get()

        if next_page:
            absolute_url = f'http://quotes.toscrape.com{next_page}'
            yield SplashRequest(url = absolute_url, 
                                  callback=self.parse,
                                  headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'},
                                  endpoint="execute", 
                                  args={'lua_source':self.script})

# IN SETTINGS FILE (settings.py) THERE'S NEED TO MAKE SOME CHANGES:
# SPIDER_MIDDLEWARES = {
#     'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
# }

# DOWNLOADER_MIDDLEWARES = {
#     'scrapy_splash.SplashCookiesMiddleware': 723,
#     'scrapy_splash.SplashMiddleware': 725,
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
# }

# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# SPLASH_URL = "http://localhost:8050/"

# FEED_EXPORT_ENCODING = 'utf-8'