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


class CDCSpider(CommonSpider):
    name = 'cdc_fr'

    allowed_domains = ['www.comptoirdescotonniers.com']
    BASE_URL = "https://www.comptoirdescotonniers.com"

    def start_by_product_category(self):
        """
        从产品分类里爬取数据
        :return:
        """
        product_category = self.product_category
        args = '?sz=250'

        for url in product_category.keys():
            list_url = url + args
            meta = {
                "category_name": product_category.get(url),
                "referer": url,

            }
            yield scrapy.Request(list_url, meta=meta, callback=self.parse_product_list,
                                 errback=self.start_request_error, dont_filter=True)

    def parse_product_list(self, response):
        product_list_xpath = '//ul[@class="swatch-list"]/li/a'
        data = response.xpath(product_list_xpath)

        for item in data:
            detail_url = self.BASE_URL + item.attrib.get("href")
            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": detail_url,
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "callback": self.parse_product_detail,
            }
            for task in self.request_product_detail(**item_data):
                yield task

    def parse_product_detail(self, response):
        size_xpath = '//li[@class="selectable variation-group-value c-variations__size-item"]/a'
        data_xpath = '//script[@type="application/ld+json"]/text()'
        desc_xpath = '//div[@itemprop="description"]/p'

        size_list = []
        if response.xpath(size_xpath):
            for node in response.xpath(size_xpath):
                size_list.append(node.attrib.get("data-size"))
        json_data = response.xpath(data_xpath).get()
        description = response.xpath(desc_xpath).get()
        product_info = json.loads(json_data)
        sku = product_info.get("sku")
        brand = product_info.get("brand")
        color = product_info.get("color")
        title = product_info.get("name")
        images = product_info.get("image")
        price = product_info.get("offers").get("price")

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
            "brand": brand
        }
        if item_data:
            yield ProductDetailItem(**item_data)
