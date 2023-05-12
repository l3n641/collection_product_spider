import json
import scrapy
from .. import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from ..common_spider import CommonSpider
import json
from urllib.parse import urlparse


class StussySpider(CommonSpider):
    name = 'stussy'
    allowed_domains = ['www.stussy.com']
    BASE_URL = "https://www.stussy.com/"

    def parse_product_list(self, response):
        urls_pattern = 'var collectionAllProducts =(.*);'
        data = response.selector.re_first(urls_pattern)
        json_data = json.loads(data)
        for item in json_data:
            response.meta["info"] = item
            link = self.BASE_URL + f"/products/{item.get('handle')}?variant={item.get('variants')[0].get('id')}"
            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": link,
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "callback": self.parse_product_detail,
            }
            for task in self.request_product_detail(**item_data):
                yield task