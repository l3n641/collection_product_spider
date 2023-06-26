import html
import json
import scrapy
from .. import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from ..common_spider import CommonSpider
import json
from urllib.parse import urlparse


class Spider(CommonSpider):
    name = 'dillards'
    allowed_domains = ['www.dillards.com']
    BASE_URL = "https://www.dillards.com"

    def start_requests(self):
        url = 'https://www.dillards.com/p/gianni-bini-zannah-rhinestone-embellished-mules/514502230'
        yield scrapy.Request(url, callback=self.parse_product_detail, errback=self.start_request_error,
                             dont_filter=True)

    def parse_product_detail(self, response):
        init_data_pattern = "window.__INITIAL_STATE__ = (.*);"
        init_data_str = response.selector.re_first(init_data_pattern)
        if init_data_str:
            data = json.loads(init_data_str)
            print(data)
