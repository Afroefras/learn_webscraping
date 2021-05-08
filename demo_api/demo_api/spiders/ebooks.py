import scrapy
from scrapy.exceptions import CloseSpider
import json

class BooksSpider(scrapy.Spider):
    name = 'ebooks'
    allowed_domains = ['openlibrary.org']
    start_urls = ['http://openlibrary.org/subjects/picture_books.json?limit=12&offset=12/']

    increment = 12
    offset = 0

    def parse(self, response):

        if response.status == 500:
            raise CloseSpider('Last page reached!')

        resp = json.loads(response.body)
        for ebook in resp.get('works'):
            yield {
                'title':ebook.get('title'),
                'author':ebook.get('authors')[0].get('name'),
                'status':ebook.get('availability').get('status'),
                'collection':ebook.get('ia_collection'),
                'subject':ebook.get('subject'),
                'cover_id':ebook.get('cover_id'),
            }

        self.offset += self.increment
        yield scrapy.Request(
            url = f'http://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.offset}/',
            callback = self.parse
        )
