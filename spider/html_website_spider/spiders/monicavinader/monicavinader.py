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


class MonicaVinaderSpider(CommonSpider):
    name = 'monicavinader'
    allowed_domains = ['www.monicavinader.com']
    BASE_URL = "https://www.monicavinader.com"

    def parse_product_list(self, response):
        product_list_xpath = '//div[@class="l-one-quarter ph-one-half"]//button'
        next_page_url_xpath = '//div[@class="pagination__links"]/a[last()]'

        products = response.xpath(product_list_xpath)
        for item in products:
            detail_url = self.BASE_URL + item.get("data-url")
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

        next_node = response.xpath(next_page_url_xpath)
        next_url = self.BASE_URL + next_node.attri.get("href")
        if next_url != response.url:
            yield scrapy.Request(next_url, meta=response.meta, callback=self.parse_product_list)

    def parse_product_detail(self, response):
        title_xpath = '//h1[@class="product-details__title"]/text()'
        price_xpath = '//meta[@ property="product:price:amount" ]'
        color_xpath = '//p[@class="product-details__subtitle"]/text()'
        image_xpath = '//figure[@class="product-gallery__image product-gallery__image--overlay"]/p[@class="js-main-gallery-image-zoom"]'
        title = response.xpath(title_xpath).get()
        price = response.xpath(price_xpath).attri.get("content")
        sku = hashlib.md5(response.url.encode(encoding='UTF-8')).hexdigest()
        color = response.xpath(color_xpath).get()
        image_node = response.xpath(image_xpath)
        images = []
        for node in image_node:
            images.append(node.attri.get("data-zoom"))
        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": response.url,
            "category_name": response.meta.get("category_name"),
            "sku": sku,
            "color": color,
            "size": [],
            "img": images,
            "price": price,
            "title": title,
            "dade": datetime.now(),
            "basc": description,
            "brand": ""
        }
        if item_data:
            yield ProductDetailItem(**item_data)
