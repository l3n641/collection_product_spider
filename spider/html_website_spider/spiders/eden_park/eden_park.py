import json
import scrapy
from .. import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from ..common_spider import CommonSpider
import json
from urllib.parse import urlparse, parse_qsl
from urllib.parse import urlencode
import html
import requests
import hashlib


class EdenParkSpider(CommonSpider):
    name = 'edanpark_fr'
    allowed_domains = ['www.eden-park.com']
    BASE_URL = "https://www.eden-park.com"

    def parse_product_list(self, response):
        product_list_pattern = 'collectionAllProducts =(.*);'
        data = response.selector.re_first(product_list_pattern)
        data = json.loads(data)
        for item in data:
            detail_url = self.BASE_URL + "/products/" + item.get("handle")
            yield scrapy.Request(detail_url, callback=self.parse_product_list2, meta=response.meta, dont_filter=True)

    def parse_product_list2(self, response):
        list_path = '//div[@class="paired_list"]/a'

        if response.xpath(list_path):
            for item in response.xpath(list_path):
                detail_url = self.BASE_URL + item.attrib.get("href")
                item_data = {
                    "category_name": response.meta.get("category_name"),
                    "detail_url": detail_url,
                    "referer": response.meta.get("referer"),
                    "page_url": response.url,
                    "meta": response.meta,
                    "callback": self.parse_product_detail,
                    "dont_filter": True,
                }
                for task in self.request_product_detail(**item_data):
                    yield task
        else:
            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": response.url,
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "callback": self.parse_product_detail,
                "dont_filter": True,
            }
            for task in self.request_product_detail(**item_data):
                yield task

    def parse_product_detail(self, response):
        title_xpath = '//meta[@property="og:title"]'
        price_xpath = '//meta[@property="og:price:amount"]'
        description_xpath = '///span[@class="description"]'
        sku_path = '//span[@class="product_id"]/text()'
        size_xpath = '//span[@ class="Taille"]/text()'
        main_image_xpath = '//meta[@property="og:image"]'
        extra_image_xpath = '//span[@class="alternate_image_url"]/text()'

        title = response.xpath(title_xpath).attrib.get("content")
        sku = response.xpath(sku_path).get()
        price = response.xpath(price_xpath).attrib.get("content").replace(",", ".")
        description = response.xpath(description_xpath).get()

        size_item = response.xpath(size_xpath)
        size_list = []

        if size_item:
            for item in size_item:
                size = html.unescape(item.get().strip())
                size_list.append(size)

        images = []
        node = response.xpath(main_image_xpath)
        images.append(node.attrib.get("content").replace("http://", "https://"))
        for node in response.xpath(extra_image_xpath):
            src = "https:" + node.get()
            images.append(src)

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": response.url,
            "category_name": response.meta.get("category_name"),
            "sku": sku,
            "color": "",
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
