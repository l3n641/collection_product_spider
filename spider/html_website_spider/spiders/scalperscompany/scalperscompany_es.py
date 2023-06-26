import json
import requests
import scrapy
from ..common_direct_spider import CommonDirectSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime
import lxml
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qsl


class ScalpersEsSpider(CommonDirectSpider):
    name = 'scalpers_es'
    allowed_domains = ['scalperscompany.com']
    base_url = "https://scalperscompany.com"

    def parse_product_list(self, response, **kwargs):
        product_url_xpath = '//div[@class="ProductItem__Wrapper"]/a'
        next_page_xpath = '//link[@rel="next"]'
        product_info = response.xpath(product_url_xpath)

        for item in product_info:

            detail_url = self.base_url + item.attrib.get("href")
            item_data = {
                "category_name": response.meta.get("category_name", ""),
                "detail_url": detail_url,
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "callback": self.parse_product_detail,
            }

            for task in self.request_product_detail(**item_data):
                yield task

        next_node = response.xpath(next_page_xpath)

        if next_node:
            next_url = self.base_url + next_node.attrib.get("href")
            yield scrapy.Request(next_url, meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error)

    def parse_product_detail(self, response):
        product_info_pattern = 'window.SwymProductInfo.product =(.*);'
        color_xpath = '//li[@ class="HorizontalList__Item"]/a[@class="ColorSwatch ColorSwatch--medium  ColorSwatch__Current"]'

        data_str = response.selector.re_first(product_info_pattern)
        product_data = json.loads(data_str)

        title = product_data.get("title")
        sku = product_data.get("handle")
        price = product_data.get("price") / 100
        description = product_data.get("description")
        color = response.xpath(color_xpath).attrib.get("data-tooltip")

        images = []
        for item in product_data.get("images"):
            src = "https:" + item
            images.append(src.replace(".jpg", "_1400x.jpg"))

        sizes = []
        for item in product_data.get("variants"):
            sizes.append(item.get("option2"))

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": response.url,
            "category_name": response.meta.get("category_name", ""),
            "sku": sku,
            "color": color,
            "size": sizes,
            "img": images,
            "price": price,
            "title": title,
            "dade": datetime.now(),
            "basc": description,
            "brand": "Scalpers"
        }

        yield ProductDetailItem(**item_data)

    def start_requests1(self):
        url = 'https://scalperscompany.com/collections/mujer-nueva-coleccion-jerseis-cardigans'
        yield scrapy.Request(url, callback=self.parse_product_list, errback=self.start_request_error,
                             dont_filter=True)
