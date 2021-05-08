# THE ORIGINAL WEBPAGE WAS HACKED, 
# THE ONE USED IN THIS SCRIPT DOES NOT HAVE ALL THE REQUIREMENTS IN ORDER TO MAKE THIS CODE RUNS CORRECTLY,
# ALTHOUGH IT IS IMPORTANT TO KNOW HOW THE STRUCTURE WORKS.

import scrapy
from scrapy_splash import SplashRequest


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['web.archive.org/']

    script = '''
        function main(splash, args)

            -- Override User-Agent, just for not getting caught scraping :P
            splash:on_request(
                function(request)
                request:set_header('User-Agent',"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36")
                end)
            
            -- Disable private mode
            splash.private_mode_enabled = false
            
            -- Go to the url
            assert(splash:go(args.url))
            -- It's important to wait in order to get the correct result
            assert(splash:wait(2))
            
            -- Select all elements with certain atribute
                rur_tab = splash:select_all(".filterPanelItem___2z5Gb ")
            -- Click just on the fifth one
            rur_tab[5]:mouse_click()
            assert(splash:wait(2))
            -- Watch all over the page
            splash:set_viewport_full()
            
            return {
                html = splash:html(),
                png = splash:png(),
                -- Data from page searched
                har = splash:har(),
            }
            end
    '''

    def start_requests(self):
        yield SplashRequest(
            url="https://web.archive.org/web/20200116052415/https://www.livecoin.net/en",
            callback=self.parse, endpoint="execute", args={'lua_source':self.script}
        )

    def parse(self, response):
        for currency in response.xpath('//div[contains(@class,"ReactVirtualized__Table__row tableRow___3EtiS ")]'):
            yield {
                'pair':currency.xpath('.//div/div/text()').get(),
                'volume':currency.xpath('.//div[2]/span/text()').get(),
                'last_price':currency.xpath('.//div[3]/span/text()').get(),
                'change':currency.xpath('.//div[4]/span/span/text()').get(),
                'high':currency.xpath('.//div[5]/span/text()').get(),
                'low':currency.xpath('.//div[6]/span/text()').get()
            }