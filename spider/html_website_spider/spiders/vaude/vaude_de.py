import json
import requests
import scrapy
from ..common_direct_spider import CommonDirectSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime
import lxml
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qsl


class VaudeDeSpider(CommonDirectSpider):
    name = 'vaude_de'
    allowed_domains = ['vaude.com']
    base_url = "https://www.vaude.com"

    def parse_product_list(self, response, **kwargs):
        product_list_xpath = '//ul[@ class="product--details-pictureslider"]/li/a'
        next_page_xpath = '//a[@class="paging--link paging--next"]'
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

        if next_nodes := response.xpath(next_page_xpath):
            for node in next_nodes:
                next_url = self.base_url + node.attrib.get("href")
                yield scrapy.Request(next_url, meta=response.meta, callback=self.parse_product_list,
                                     errback=self.start_request_error)

    def parse_product_detail(self, response):
        title_xpath = '//h1[@class="product--title"]/text()'
        price_xpath = '//meta[@itemprop="price"]'
        color_xpath = '//strong[@ class="color--selected"]/text()'
        desc_xpath = '//div[@class="description-column"]'
        sku_xpath = '//div[@data-sku]'
        size_xpath = '//div[@ class="variant--group variant--sizes"]//div[@data-option]'
        image_xpath = '//div[@class="image-slider--container"]//span[@class="image--element lens--supported"]'
        title = response.xpath(title_xpath).get().strip()
        price = response.xpath(price_xpath).attrib.get("content").strip()
        description = response.xpath(desc_xpath).get()
        color = response.xpath(color_xpath).get()
        sku = response.xpath(sku_xpath).attrib.get("data-sku")

        images = []
        for item in response.xpath(image_xpath):
            image = item.attrib.get("data-img-large")
            images.append(image)

        sizes = []
        size_nodes = response.xpath(size_xpath)
        for node in size_nodes:
            sizes.append(node.attrib.get("data-option"))

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
            "brand": "Vaude"
        }

        yield ProductDetailItem(**item_data)

    def start_requests1(self):
        url = 'https://www.vaude.com/de-DE/Herren/Bekleidung/Hosen/Monviso-Softshell-Hose-Herren?number=429821460460'
        yield scrapy.Request(url, callback=self.parse_product_detail, errback=self.start_request_error,
                             dont_filter=True)
