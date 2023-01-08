import json

import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
from html import unescape
from urllib.parse import urlencode
from datetime import datetime


class TheKooplesSpider(CommonSpider):
    name = 'the_koople'
    allowed_domains = ['thekooples.com']
    base_url = "https://www.thekooples.com"

    custom_settings = {
        "CONCURRENT_REQUESTS": 4,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
    }

    def parse_product_list(self, response, **kwargs):
        product_url_xpath = '//a[@ class="link-url"]'
        next_page_xpath = '//a[@id="next-page-href"]'

        product_info = response.xpath(product_url_xpath)

        for item in product_info:

            detail_url = self.base_url + item.attrib.get("href")
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

        next_page_node = response.xpath(next_page_xpath)
        if next_page_node:
            next_url = self.base_url + next_page_node.attrib.get("href")
            yield scrapy.Request(next_url, meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error)

    def parse_product_detail(self, response):
        title_xpath = '//h1[@class="product-name"]/text()'
        img_xpath = '//div[@id="panzoom-element"]/img'
        size_xpath = '//span[@class="size-field  selectable"]'
        product_info_xpath = '//script[@type="application/ld+json]'

        data_str = response.xpath(product_info_xpath)[2]
        product_data = json.loads(data_str)
        title = product_data.get("name")
        sku = product_data.get("sku")
        description = product_data.get("description")
        color = product_data.get("color")
        price = product_data.get("offers").get('price')

        images = []
        for node in response.xpath(img_xpath):
            src = node.attrib.get("src")
            images.append(src)

        sizes = []
        for node in response.xpath(size_xpath):
            sizes.append(node.get())

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": response.url,
            "category_name": response.meta.get("category_name"),
            "sku": sku,
            "color": color,
            "size": sizes,
            "img": images,
            "price": price,
            "title": title,
            "dade": datetime.now(),
            "basc": description,
            "brand": product_data.get("brand")
        }

        yield ProductDetailItem(**item_data)


def start_requests(self):
    url = 'https://www.thekooples.com/fr/fr_FR/femme/pret-a-porter/manteaux-et-blousons/doudoune-vinyle-oversize-noire-bretelles-a-logo-FDOU25006KBLA01.html'
    yield scrapy.Request(url, callback=self.parse_product_detail, errback=self.start_request_error,
                         dont_filter=True)
