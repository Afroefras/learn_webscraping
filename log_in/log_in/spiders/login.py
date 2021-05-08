import scrapy
from scrapy import FormRequest

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/account/login']

    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formid = 'username',
            formdata = {
                'username':'efraisma.ef7@gmail.com',
                'password':'Test7!',
                'redirect':'/',
                'debug_token':'',
                'login':'Log In'
            },
            callback = self.after_login
        )

    def after_login(self,response):
        print('Logged in!!!')
