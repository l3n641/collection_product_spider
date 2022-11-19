import json
import scrapy
from .. import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from ..common_spider import CommonSpider
import json
from urllib.parse import urlparse


class OlukaiSpider(CommonSpider):
    name = 'olukai'
    allowed_domains = ['olukai.com']
    BASE_URL = "https://olukai.com"

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

    def parse_product_detail(self, response):
        other_info = response.meta.get("info")
        title_xpath = '//h1[@class="product__name"]/text()'
        desc_xpath = '//p[@class="product__description-translation"]/text()'
        title = response.xpath(title_xpath).get()
        description = response.xpath(desc_xpath).get()
        sku = other_info.get("id")
        price = other_info.get("price") / 100
        options = other_info.get("options")
        color_index = None
        size_index = None
        for index, opt in enumerate(options):
            if opt == "Color":
                color_index = index

            if opt == "Size":
                size_index = index

        color = ""
        if color_index is not None:
            color = other_info.get("variants")[0].get("options")[color_index]

        size_list = []
        if size_index:
            for var in other_info.get("variants"):
                size_list.append(var.get("options")[size_index])
        images = []
        for image in other_info.get("images"):
            img_url = f"https:{image}"
            images.append(img_url)

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
