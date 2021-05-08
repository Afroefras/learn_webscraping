import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class QuotesSpiderSelenium(scrapy.Spider):
    name = 'quotes_selenium'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js']

    def __init__(self):

        # Open no browser but still works
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # Request to the specifid URL
        driver = webdriver.Chrome(executable_path = './chromedriver', options = chrome_options)
        driver.set_window_size(1920,1080)
        driver.get('http://quotes.toscrape.com/js')

        # Extract the html code
        self.html = driver.page_source

        # It's a good practice to close the request
        driver.close()

    def parse(self, response):
        resp = Selector(text = self.html)
        for quote in resp.xpath('//div[@class = "quote"]'):
            yield {
                'quote': quote.xpath('.//span[@class="text"]/text()').get(),
                'author': quote.xpath('.//span[2]/small[@class="author"]/text()').get(),
                'tags': quote.xpath('.//div[@class="tags"]/a/text()').getall()
            }