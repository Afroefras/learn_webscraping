import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = 'quotes_api'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):
        resp = json.loads(response.body)
        for quote in resp.get('quotes'):
            yield {
                'author':quote.get('author').get('name'),
                'tags':quote.get('tags'),
                'text':quote.get('text')
            }

        if resp.get('has_next'):
            next_page_number = resp.get('page') + 1
            yield scrapy.Request(
                url = f'http://quotes.toscrape.com/api/quotes?page={next_page_number}', 
                callback = self.parse
            )
