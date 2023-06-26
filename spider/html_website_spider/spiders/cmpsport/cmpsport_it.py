import json
import requests
import scrapy
from ..common_direct_spider import CommonDirectSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime
import lxml
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qsl
import re


class CmpSportSpider(CommonDirectSpider):
    name = 'cmpsport_it'
    allowed_domains = ['cmpsport.com']
    base_url = "https://www.cmpsport.com/"

    def parse_product_list(self, response, **kwargs):
        product_list_xpath = '//div[@ class="product-item-info"]/a'
        next_page_xpath = '//link[@rel="next"]'
        for item in response.xpath(product_list_xpath):

            detail_url = item.attrib.get("href")
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

        if next_node := response.xpath(next_page_xpath):
            next_url = next_node.attrib.get("href")
            yield scrapy.Request(next_url, meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error)

    def parse_product_detail(self, response):
        title_xpath = '//meta[@ name="title"]'
        config_pattern = '"jsonConfig":(.*),'
        desc_xpath = '//div[@itemprop="description"]'
        spu_xpath = '//form[@data-product-sku]'
        title = response.xpath(title_xpath).attrib.get("content")
        description = response.xpath(desc_xpath).get()
        spu = response.xpath(spu_xpath).attrib.get("data-product-sku")
        config_str = response.selector.re_first(config_pattern)
        config = json.loads(config_str)
        product_attribs = config.get("attributes")
        price = config.get("prices").get("finalPrice").get("amount")
        color_options = []
        sizes = []
        for key in product_attribs:
            attrib = product_attribs.get(key)
            if attrib.get("code") == "color":
                color_options = attrib.get("options")

            if attrib.get("code") == "size":
                for opt in attrib.get("options"):
                    sizes.append(opt.get("label"))

        for opt in color_options:
            if opt.get("products"):
                color = opt.get("label")
                color_id = opt.get("id")
                pid = opt.get("products")[0]
                image_list = config.get("images").get(pid)
                images = []
                for img in image_list:
                    images.append(img.get("full"))

                sku = spu + "_" + color_id
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
                    "brand": "CMP"
                }

                yield ProductDetailItem(**item_data)

    def start_requests1(self):
        url = 'https://www.cmpsport.com/it/gilet-nylon-con-imbottitura-3m-thinsulate-da-donna-31z5376b'
        yield scrapy.Request(url, callback=self.parse_product_detail, errback=self.start_request_error,
                             dont_filter=True)
