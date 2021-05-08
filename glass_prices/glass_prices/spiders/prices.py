import scrapy


class PricesSpider(scrapy.Spider):
    name = 'prices'
    allowed_domains = ['www.glassesshop.com']

    def start_requests(self):
        yield scrapy.Request(url='https://www.glassesshop.com/bestsellers',
                             callback=self.parse,
                             headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'})

    def parse(self, response):
        for glasses in response.xpath('//div[@id = "product-lists"]/div'):
            yield {
                'product_link': glasses.xpath('.//div[@class = "product-img-outer"]/a/@href').get(),
                'image_front': glasses.xpath('.//div[@class = "product-img-outer"]/a/img/@data-src').get(),
                'image_side': glasses.xpath('.//div[@class = "product-img-outer"]/a/img[2]/@data-src').get(),
                'colors': glasses.xpath('.//div[@class = "p-title-block"]/div/div/div/span/@title').get(),
                'title': glasses.xpath('.//div[@class = "p-title-block"]/div[2]/div/div/div/a/text()').get(),
                'price': glasses.xpath('.//div[@class = "p-title-block"]/div[2]/div/div[2]/div/div/span/text()').get(),
            }

            for i in range(1,5):
                yield scrapy.Request(url=f'https://www.glassesshop.com/bestsellers?page={i+1}',
                                           callback=self.parse,
                                           headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'})