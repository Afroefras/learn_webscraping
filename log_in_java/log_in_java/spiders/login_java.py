import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest
 
 
class QuotesLoginSpider(scrapy.Spider):
    name = 'login_java'
    allowed_domains = ['quotes.toscrape.com']
    
    script = '''
        function main(splash, args)
          assert(splash:go(args.url))
          assert(splash:wait(3))
          return splash:html()
        end
    '''
    
    def start_requests(self):
        yield SplashRequest(
            url='https://quotes.toscrape.com/login',
            endpoint='execute',
            args = {
                'lua_source': self.script
            },
            callback=self.parse
        )
 
    def parse(self, response):
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        yield SplashFormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
                'csrf_token': csrf_token,
                'username': 'admin',
                'password': 'admin'
            },
            callback=self.after_login
        )
    
    def after_login(self, response):
        if response.xpath("//a[@href='/logout']/text()").get():
            print('logged in')

# ADD TO settings.py:
# USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'

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