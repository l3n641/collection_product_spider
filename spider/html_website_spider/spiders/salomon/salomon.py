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


class SalomonFrSpider(CommonSpider):
    name = 'salomon_fr'
    allowed_domains = ['www.salomon.com']
    BASE_URL = "https://www.salomon.com"
    color_id = "2109"

    custom_settings = {
        'COOKIES_ENABLED': False,
        "CONCURRENT_REQUESTS": 4,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
    }

    def parse_product_list(self, response):
        product_info_xpath = '//div[@class="product-tile_head"]/a[@ref="linkHead"]'
        next_page_xpath = '//a[@class="product-tile-load-more_link"]'
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
        image_args = '?dpr=1&fit=cover&orient=1&optimize=low&bg-color=f5f5f5&format=pjpg&auto=webp&pad=0&width=1200'
        title_xpath = '//meta[@property="og:title"]'
        desc_xpath = '//div[@class="product-description_text"]'
        data_xpath = '//div[@class="swatch-opt"]'
        size_xpath = '//div[@class="size-selection_sizes "]/ul/li[@class="input-size"]/label/span/text()'
        data_str = response.xpath(data_xpath).attrib.get("data-json-config")
        json_data = json.loads(data_str)
        product_id = json_data.get('productId')
        attributes = json_data.get("attributes")
        colors = attributes.get(self.color_id)
        images_info = json_data.get("images")
        option_prices = json_data.get("optionPrices")
        title = response.xpath(title_xpath).attrib.get("content")
        desc = response.xpath(desc_xpath).get()
        size_list = []
        for node in response.xpath(size_xpath):
            size = node.get().strip()
            size_list.append(size)

        if colors and (options := colors.get("options")):
            for opt in options:
                color_id = opt.get("id")
                color = opt.get("label")
                sku = product_id + "_" + color_id
                pid = opt.get("products")[0]
                image_info = images_info.get(pid)
                price = option_prices.get(pid).get("finalPrice").get("amount")
                images = []
                for item in image_info:
                    if item.get("type") == "image":
                        image_url = item.get("value") + image_args
                        images.append(image_url)

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
