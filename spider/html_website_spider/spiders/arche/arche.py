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


class ArcheFrSpider(CommonSpider):
    name = 'arche_fr'
    allowed_domains = ['www.arche.com']
    BASE_URL = "https://www.arche.com"

    def parse_product_list(self, response):
        product_info_xpath = '//div[@class="product-item-info" ]/a'
        next_page_xpath = '//link[@rel="next"]'
        product_info = response.xpath(product_info_xpath)

        for item in product_info:
            detail_url = item.attrib.get("href")

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

        next_page_url = response.xpath(next_page_xpath).attrib.get("href")
        if next_page_url:
            yield scrapy.Request(next_page_url, meta=response.meta, callback=self.parse_product_list)

    def parse_product_detail(self, response):
        title_xpath = '//h1[@itemprop="name"]/text()'
        sku_xpath = '//div[@class="ref sku"]/text()'
        price_xpath = '//meta[@itemprop="price"]'
        desc_xpath = '//div[@class="product attribute description"]/div[@class="value"]/p'
        img_xpath = '//picture[@class="swiper-slide"]/source/img'
        size_pattern = 'AEC.SUPER =(.*);'

        title = response.xpath(title_xpath).get()
        sku = response.xpath(sku_xpath).get().replace("*", "-")
        price = response.xpath(price_xpath).attrib.get("content")

        desc = response.xpath(desc_xpath).get()
        size_list = []
        size_info_str = response.selector.re_first(size_pattern)
        size_info = json.loads(size_info_str)
        if size_info and size_info[0].get("code") == "size":
            for node in size_info[0].get("options"):
                size = node.get("label").strip()
                size_list.append(size)

        images = []
        for img in response.xpath(img_xpath):
            images.append(img.attrib.get("data-src"))

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
            "basc": desc,
            "brand": ""
        }

        if item_data:
            yield ProductDetailItem(**item_data)
