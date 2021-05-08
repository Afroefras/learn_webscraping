import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['web.archive.org']

    def start_requests(self):
        yield scrapy.Request(url='https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html',
                             callback=self.parse,
                             headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'})

    def parse(self, response):
        for product in response.xpath('//ul[@class = "productlisting-ul"]/div/li'):
            yield {
                'title': product.xpath('.//a[2]/text()').get(),
                'stars': product.xpath('.//div/a/text()').get(),
                'normal_price': product.xpath('.//div[2]/span[2]/text()').get(),
                'discount': product.xpath('.//a/div/div/text()').get(),
                'special_price': product.xpath('.//div[2]/span/text()').get()
            }

            next_page = response.xpath('//a[@class = "nextPage"]/@href').get()
            if next_page:
                yield scrapy.Request(url=next_page,
                                     callback=self.parse, 
                                     headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'})