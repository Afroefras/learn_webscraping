import scrapy
from scrapy.http import FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['openlibrary.org']
    start_urls = ['http://openlibrary.org/account/login/']

    def parse(self, response):
        yield FormRequest.from_response(response=response,
                                        formxpath='//form[@id = "register"]', formdata={
                                            'username': 'efraisma.ef7@gmail.com',
                                            'password': 'Test7!',
                                            'redirect': '/',
                                            'debug_token': '',
                                            'login': 'Log In'
                                        }, callback=self.after_login)

    def after_login(self, response):
        for book in response.xpath('//div[@class = "book carousel__item"]'):
            yield {
                'title': book.xpath('.//img/@title').get(),
                'img_url': book.xpath('.//img/@src').get(),
            }
