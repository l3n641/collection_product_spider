import json
import requests
import scrapy
from ..common_direct_spider import CommonDirectSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime
import lxml
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qsl


class LaSportivaSpider(CommonDirectSpider):
    name = 'lasportiva_it'
    allowed_domains = ['lasportiva.com']
    base_url = "https://www.lasportiva.com"

    def parse_product_list(self, response, **kwargs):
        product_list_xpath = '//div[@class="product-item-info"]/a'
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
        color_xpath = '//div[@class="swatch-attribute color"]/a[@class="selected"]'
        title_xpath = '//span[@data-ui-id="page-title-wrapper"]/text()'
        image_pattern = '"data": (.*),'
        price_xpath = '//meta[@itemprop="price" ]'
        desc_xpath = '//div[@itemprop="description"]'
        sku_xpath = '//form[@data-product-sku]'
        title = response.xpath(title_xpath).get()
        price = response.xpath(price_xpath).attrib.get("content")
        description = response.xpath(desc_xpath).get()
        color = response.xpath(color_xpath).attrib.get("title").split("-")[-1]
        sku = response.xpath(sku_xpath).attrib.get("data-product-sku")
        image_info_str = response.selector.re_first(image_pattern)
        images_list = json.loads(image_info_str)
        images = []
        if images_list:
            for item in images_list:
                if item.get("type") == "image":
                    image = item.get("img").replace('&height=700&width=700&canvas=700:700',
                                                    '&height=1200&width=1200&canvas=1200:1200')
                    images.append(image)

        sizes = []

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
            "brand": "La Sportiva"
        }

        yield ProductDetailItem(**item_data)

    def start_requests1(self):
        url = 'https://www.lasportiva.com/it/cyklon-uomo-verde-46w720314'
        yield scrapy.Request(url, callback=self.parse_product_detail, errback=self.start_request_error,
                             dont_filter=True)
