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


class WolfordshopNlSpider(CommonSpider):
    name = 'wolfordshop_nl'
    allowed_domains = ['www.wolfordshop.nl']
    BASE_URL = "https://www.wolfordshop.nl"
    image_prefix = "https://www.wolfordshop.nl/dw/image/v2/BBCH_PRD"

    def parse_product_list(self, response):
        product_info_xpath = '//div[@class="product-color"]/div[@class="product-variation-list js-product-variations-list"]//a[@class="product-variation-link js-product-variation-link "]'
        next_page_xpath = '//a[@class="page-next"]'
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
        image_suffix = '?sw=1269&sh=1690&sm=fit'
        title_xpath = '//meta[@property="og:title"]'
        desc_xpath = '//meta[@property="og:description"]'
        image_xpath = '//div[@class="pdp-main-media"]/div[@class="pdp-main__image js-main-product-image"]/figure/img'
        sku_xpath = '//input[@id="variationGroupId"]'
        size_xpath = '//select[@id="va-size"]/option'
        color_xpath = '//div[@class="product-color"]/span[@class="selected-variant"]/text()'
        price_xpath = '//div[@id="js-product-properties-block"]//div[@ class="product-pricing js-product-pricing"]'

        title = response.xpath(title_xpath).attrib.get("content")
        sku = response.xpath(sku_xpath).attrib.get("value").replace(".", "_")
        desc = response.xpath(desc_xpath).attrib.get("content")
        size_list = []
        for node in response.xpath(size_xpath)[1:]:
            size = node.attrib.get("data-size")
            if size:
                size_list.append(size)
            else:
                size_list.append(node.attrib.get("value"))

        images = []
        for node in response.xpath(image_xpath):
            src = node.attrib.get("data-src")
            if not src.startswith("https"):
                src = self.image_prefix + src + image_suffix
            images.append(src)
        color = response.xpath(color_xpath).get()

        price = response.xpath(price_xpath).attrib.get("data-price")

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
            "basc": desc,
            "brand": ""
        }

        if item_data:
            yield ProductDetailItem(**item_data)
