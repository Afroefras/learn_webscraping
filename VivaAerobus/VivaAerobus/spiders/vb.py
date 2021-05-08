import scrapy


class VbSpider(scrapy.Spider):
    name = 'vb'

    payload = '''
        {"journey":{"fullRoute":"PVR>MEX|MEX>PVR","priceSpecification":{"priceBeforeTaxesAndFees":null,"totalPrice":439,"currencyCode":"MXN","currencySymbol":"MXN","isSoldOut":false},"passenger":{"count":1,"seniorCount":0,"adultCount":1,"youngAdultCount":0,"childCount":0,"infantInLapCount":0,"infantInSeatCount":0},"passengerDetails":[{"category":"adult","mappedTo":"adultCount","count":1}],"outboundFlight":{"boundType":"OUTBOUND","priceSpecification":{"priceBeforeTaxesAndFees":null,"totalPrice":229,"currencyCode":"MXN","currencySymbol":"MXN","isSoldOut":false},"flightType":"DOMESTIC","route":"PVR>MEX","fareClassInput":"Zero","fareClass":"ECONOMY","departureAirportIataCode":"PVR","arrivalAirportIataCode":"MEX","departureDate":"2021-03-24"},"journeyType":"ROUND_TRIP","flightType":"DOMESTIC","airline":{"name":"Viva Aerobus","iataCode":"VB"},"inboundFlight":{"boundType":"INBOUND","priceSpecification":{"priceBeforeTaxesAndFees":null,"totalPrice":210,"currencyCode":"MXN","currencySymbol":"MXN","isSoldOut":false},"flightType":"DOMESTIC","route":"MEX>PVR","fareClassInput":"Zero","fareClass":"ECONOMY","departureAirportIataCode":"MEX","arrivalAirportIataCode":"PVR","departureDate":"2021-03-24"},"departureDate":"2021-03-24","returnDate":"2021-03-24"},"page":{"name":"Search Result Page","url":"https://www.vivaaerobus.com/mx/flight/booking","hostName":"www.vivaaerobus.com","languageIsoCode":"es","siteEdition":"es"},"device":{"category":"DESKTOP","screenResolution":"2880x1800","operatingSystem":"MacOS"},"metadata":{"app":{"name":"Farenet","version":"vb_v3.1","datasource":"IBE_FLIGHT_SELECTION"},"emcid":null,"schemaVersion":"1.0.0"},"priceSpecification":{"currencyCode":"MXN","currencySymbol":"MXN"}}
    '''

    def start_requests(self):
        yield scrapy.Request(url='https://www.vivaaerobus.com/mx/flight/booking',
                             method='POST', 
                             body=self.payload,
                             headers={'content-type':'application/x-www-form-urlencoded','user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'})

    def parse(self, response):
        pass
