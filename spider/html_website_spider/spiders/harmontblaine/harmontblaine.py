import json

import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime

from urllib.parse import urlparse
import requests
import re


class HarmontBlaineItSpider(CommonSpider):
    name = 'harmontblaine_it'
    allowed_domains = ['harmontblaine.com']
    base_url = "https://www.harmontblaine.com"

    def parse_product_list(self, response, **kwargs):
        product_url_xpath = '//a[@id="LnkProdotto"]'
        page_xpath = '//ul[@class="pagination no_margin"]/li[@class=""]'

        product_info = response.xpath(product_url_xpath)

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

        next_page_node = response.xpath(page_xpath)
        if next_page_node:
            next_url = self.base_url + next_page_node.attrib.get("href")
            yield scrapy.Request(next_url, meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error)

    def parse_product_detail(self, response):
        title_xpath = '//span[@itemprop="name"]/text()'
        price_xpath = '//span[@class="skywalker_scheda_nome_prezzo"]/text()'
        color_xpath = '//li[@class="tassello tassello-attivo"]/img'
        desc_xpath = '//div[@id="Dettaglio"]/ul'
        img_xpath = '//ul[@class="thumbelina"]/li/a'
        size_xpath = '//div[@class="skywalker_scheda_capoabbigliamento_taglie"]//ul/li/a'
        sku_pattern = "<p>SKU:(.*?)</p>"
        other_color_xpath = '//li[@class="tassello"]/a'

        title = response.xpath(title_xpath).get()
        price = response.xpath(price_xpath).get().replace("€", "").replace(",", '.')
        sku = response.selector.re_first(sku_pattern)
        description = response.xpath(desc_xpath).root.text
        color = response.xpath(color_xpath).attrib.get("title")

        images = []
        for node in response.xpath(img_xpath):
            src = node.attrib.get("href")
            images.append(src)

        sizes = []
        for node in response.xpath(size_xpath):
            sizes.append(node.attrib.get("title"))

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
            "brand": ""
        }

        yield ProductDetailItem(**item_data)

        other_colors=response.xpath(other_color_xpath)
        for data in other_colors:
            detail_url = data.attrib.get("href")
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

    def start_requests(self):
        url = 'https://www.harmontblaine.com/it-IT-it/product_camicia-a-quadri-mini-blutaglia-s_509779001.aspx'
        yield scrapy.Request(url, callback=self.parse_product_detail, errback=self.start_request_error, )
