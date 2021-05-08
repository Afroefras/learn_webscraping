import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys


class ExampleSpider(scrapy.Spider):
    name = 'example'
    
    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://duckduckgo.com',
            wait_time = 4,
            callback = self.parse
        )

    def parse(self, response):
        # Set the webdriver
        driver = response.meta['driver']
        # Select an object
        search_input = driver.find_element_by_xpath('//input[@id = "search_form_input_homepage"]')
        # Type into this object
        search_input.send_keys('Hello world')
        # Press enter
        search_input.send_keys(Keys.ENTER)
        # Save a screenshot of the actual page
        driver.save_screenshot('screenshot_test.png')
        # Get the html code
        html = driver.page_source
        # Make it a response object
        response_obj = Selector(text = html)

        for link in response_obj.xpath('//div[@class = "result__extras__url"]/a'):
            yield {
                'URL':link.xpath('.//@href').get()
            }
