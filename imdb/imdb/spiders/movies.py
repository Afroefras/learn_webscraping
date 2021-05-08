import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MoviesSpider(CrawlSpider):
    name = 'movies'
    allowed_domains = ['imdb.com']
    # Google "my user agent" to override the request agent, just for not getting caught scraping :P
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250',
                             headers={'User-Agent': self.user_agent})

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//td[@class = "titleColumn"]/a'), callback='parse_item', follow=True, process_request='set_user_agent'),
        # If there was a button that links actual page with the next one:
        # Rule(LinkExtractor(restrict_xpaths='NEXTPAGE_XPATH'), process_request='set_user_agent'),
    )

    def set_user_agent(self, request,spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath('//div[@class = "title_wrapper"]/h1/text()').get(),
            'year': response.xpath('//span[@id = "titleYear"]/a/text()').get(),
            # Get rid of unnecesary spaces with normalize-space()
            'duration': response.xpath('normalize-space(//div[@class = "subtext"]/time/text())').get(),
            'genre': response.xpath('//div[@class = "subtext"]/a/text()').get(),
            'classif': response.xpath('normalize-space(//div[@class = "subtext"]/text())').get(),
            'release': response.xpath('//a[@title = "See more release dates"]/text()').get(),
            'rating': response.xpath('//span[@itemprop = "ratingValue"]/text()').get(),
            'users_rated': response.xpath('//span[@itemprop = "ratingCount"]/text()').get(),
            'poster_img_url': response.xpath('//div[@class = "poster"]/a/img/@src').get(),
            'movie_url': response.url,
            # Same level with /following-sibling::ELEMENT
            'budget': response.xpath('normalize-space(//h4[text() = "Budget:"]/following-sibling::text())').get(),
            'op_weekend_US': response.xpath('normalize-space(//h4[text() = "Opening Weekend USA:"]/following-sibling::text())').get(),
            'gross_US': response.xpath('normalize-space(//h4[text() = "Gross USA:"]/following-sibling::text())').get(),
            'gross_worldwide': response.xpath('normalize-space(//h4[text() = "Cumulative Worldwide Gross:"]/following-sibling::text())').get(),
            'review': response.xpath('normalize-space(//div[@class = "comment-meta"]/following-sibling::div/p/text())').get()
        }
        