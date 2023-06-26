import json
import scrapy
from .. import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from ..common_spider import CommonSpider
import json
from urllib.parse import urlparse


class ChampionSpider(CommonSpider):
    name = 'champion'
    allowed_domains = ['www.champion.com']
    BASE_URL = "https://www.champion.com/"

    def parse_product_list(self, response):
        product_list_xpath = '//a[@class="product-item-link"]'
        data = response.xpath(product_list_xpath)
        for item in data:

            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": item.attrib.get("href"),
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "callback": self.parse_product_detail,
            }
            for task in self.request_product_detail(**item_data):
                yield task

    def parse_product_detail(self, response):
        json_config_pattern = ' "jsonConfig":(.*),'
        title_xpath = '//meta[@name="title"]'
        json_config_str = response.selector.re_first(json_config_pattern)
        config = json.loads(json_config_str)
        color_id = None
        color_map = {}
        size_list = []
        for attr_id in config.get("attributes"):
            item = config.get("attributes").get(attr_id)
            if item.get("code") == "color":
                color_id = item.get("id")
                for opt in item.get("options"):
                    f_p_id = opt.get("products")[0]
                    color_map[f_p_id] = opt.get("label")

            if item.get("code") == "Size":
                for opt in item.get("options"):
                    size_list.append(opt.get("label"))

        price = config.get("prices").get("baseOldPrice").get("amount")
        title = response.xpath(title_xpath).first()

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": response.url,
            "category_name": response.meta.get("category_name"),
            "sku": sku,
            "color": color,
            "size": size_list,
            "img": images,
            "price": price,
            "title": title,
            "dade": datetime.now(),
            "basc": description,
            "brand": ""
        }
        if item_data:
            yield ProductDetailItem(**item_data)

    def start_requests(self):

        url = 'https://www.champion.com/reverse-weave-boyfriend-hoodie-embroidered-c-logo-with-multi-flowers.html'
        yield scrapy.Request(url, callback=self.parse_product_detail, errback=self.start_request_error,
                             dont_filter=True)
