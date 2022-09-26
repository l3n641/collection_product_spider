from scrapy import Spider


class SohuIpSpider(Spider):
    name = 'sohu_ip'
    allowed_domains = ['sohu.com']
    start_urls = [
        "http://pv.sohu.com/cityjson",
        "https://pv.sohu.com/cityjson",
    ]

    def parse(self, response, **kwargs):
        print(response.url, response.text)
