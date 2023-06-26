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


class DiadoraItSpider(CommonSpider):
    name = 'diadora_it'
    allowed_domains = ['www.diadora.com']
    BASE_URL = "https://www.diadora.com"
    product_detail_api = 'https://www.diadora.com/on/demandware.store/Sites-IT-Site/it_IT/Product-Variation?pid={}'

    def parse_product_list(self, response):
        product_list_xpath = '//a[@class="clickProductImagePLP"]'
        pagination_xpath = '//select[@id="select-pagination"]/option'
        product_info = response.xpath(product_list_xpath)

        for item in product_info:
            pid = item.attrib.get('data-pid')
            detail_url = self.product_detail_api.format(pid)
            yield scrapy.Request(detail_url, meta=response.meta, callback=self.parse_product_list2, dont_filter=True)

        pagination = response.xpath(pagination_xpath)
        if pagination:
            for item in pagination:
                if item.attrib.get("selected") is None and (next_page_url := item.attrib.get("data-href")):
                    yield scrapy.Request(next_page_url, meta=response.meta, callback=self.parse_product_list)

    def parse_product_list2(self, response):
        json_data = response.json()
        product_data = json_data.get("product")
        variation_attributes = product_data.get("variationAttributes")

        for attr in variation_attributes:
            if attr.get("id") == "color":
                for value in attr.get("values"):
                    detail_url = value.get("url")
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
        json_data = response.json()
        product_data = json_data.get("product")
        sku = product_data.get("id")
        brand = product_data.get("brand")
        title = product_data.get("productName")
        variation_attributes = product_data.get("variationAttributes")
        price = product_data.get("price").get("sales").get("value")
        desc = product_data.get("longDescription")
        html_url = self.BASE_URL + product_data.get("selectedProductUrl")
        color = ""
        size_list = []
        for attr in variation_attributes:
            if attr.get("id") == "color":
                color = attr.get("displayValue")

            if attr.get("id") == "size":
                for value in attr.get("values"):
                    size_list.append(value.get("displayValue"))

        images = []
        for img in product_data.get("imagesProduct"):
            if img and (src := img.get("img")):
                images.append(src.replace("?sw=1920", "?sw=1400"))

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": html_url,
            "category_name": response.meta.get("category_name"),
            "sku": sku,
            "color": color,
            "size": size_list,
            "img": images,
            "price": price,
            "title": title,
            "dade": datetime.now(),
            "basc": desc,
            "brand": brand
        }

        if item_data:
            yield ProductDetailItem(**item_data)
