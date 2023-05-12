import json
import requests
import scrapy
from ..common_direct_spider import CommonDirectSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime
import lxml
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qsl


class MaisonLabiche(CommonDirectSpider):
    name = 'maisonlabiche_fr'
    allowed_domains = ['maisonlabiche.com']
    domain = "https://www.maisonlabiche.com"

    def parse_product_list(self, response, **kwargs):
        product_list_xpath = '//a[@class="grid-product__link"]'
        for item in response.xpath(product_list_xpath):

            detail_url = self.domain + item.attrib.get("href")

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

    def parse_product_detail(self, response):
        color_xpath = '//span[@class="variant__label-info"]/span/text()'
        title_xpath = '//h1[@ class="h2 product-single__title"]/text()'
        price_xpath = '//span[@ class="product__price"]/text()'
        desc_xpath = '//div[@class="wrapper product__description"]'
        image_xpath = '//img[@ data-photoswipe-src]'
        size_xpath = '//input[@name="size"]'

        title = response.xpath(title_xpath).get().strip()
        price = response.xpath(price_xpath).get().strip().replace(",", ".").replace("€", "")
        description = response.xpath(desc_xpath).get()
        color = response.xpath(color_xpath).get().strip()
        sku = self.get_url_md5(response.url)

        image_node = response.xpath(image_xpath)

        images = []
        if image_node:
            for item in image_node:
                image = "https:" + item.attrib.get("data-photoswipe-src").replace("1800x1800.", "1200x1200.")
                images.append(image)

        size_node = response.xpath(size_xpath)

        sizes = []
        if size_node:
            for item in size_node:
                sizes.append(item.attrib.get("value"))

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
            "brand": "Maison Labiche"
        }

        yield ProductDetailItem(**item_data)

    def start_requests1(self):
        url = 'https://www.maisonlabiche.com/fr/collections/tee-shirts-femme/products/poitou-nuit-d-ete-gots-script-pointille-adulte-298'
        yield scrapy.Request(url, callback=self.parse_product_detail, errback=self.start_request_error,
                             dont_filter=True)
