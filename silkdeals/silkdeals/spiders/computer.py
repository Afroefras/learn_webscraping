import scrapy
from scrapy_selenium import SeleniumRequest

class ComputerSpider(scrapy.Spider):
    name = 'computer'
    
    def start_requests(self):
        yield SeleniumRequest(url = 'https://slickdeals.net/computer-deals/', 
                            callback = self.parse, 
                            wait_time = 3,
                            )


    def parse(self, response):
        for product in response.xpath('//li[contains(@class,"fpGridBox grid ")]'):
            yield {
                'image_url':product.xpath('.//img/@data-original').get(),
                'store':product.xpath('.//button[contains(@class,"itemStore")]/text()').get(),
                'product':product.xpath('.//span[@class = "blueprint"]/following-sibling::a/text()').get(),
                'price':product.xpath('normalize-space(.//div[@class = "itemPrice  wide "]/text())').get(),
                'likes':product.xpath('.//span[@class = "likesLabel"]/span[2]/text()').get(),
                'comments':product.xpath('.//div[contains(@class,"comments")]/span/following-sibling::span/text()').get(),
            }
        next_page = response.xpath('//a[@data-role = "next-page"]/@href').get()
        if next_page:
            absolute_url = f'https://slickdeals.net{next_page}'
            yield SeleniumRequest(url = absolute_url, callback = self.parse, wait_time = 3)