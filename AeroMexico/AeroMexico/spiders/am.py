import scrapy


class AmSpider(scrapy.Spider):
    name = 'am'
    allowed_domains = ['aeromexico.com']

    def start_requests(self):
        yield scrapy.Request(url='https://aeromexico.com/es-mx/reserva/opciones?itinerary=GDL_MTY_2021-03-21&leg=1&travelers=A1_C0_I0_PH0_PC0',
                             callback=self.parse,
                             headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'})

    def parse(self, response):
        # for vuelo in response.xpath('//table[@class="FlightOptionsGrid-table"]/tbody/tr'):
        #     yield {
        #         'departure_time':vuelo.xpath('.//div[@class="FlightOptionsTimeline-time"]/text()').get(),
        #         'departure_city':vuelo.xpath('.//div[@class="FlightOptionsTimeline-time"]/text()').get(),
        #     }
        pass