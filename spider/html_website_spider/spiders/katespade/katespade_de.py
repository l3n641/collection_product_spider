import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime
from urllib.parse import urlparse


class KatespadeDESpider(CommonSpider):
    name = 'katespade_de'
    allowed_domains = ['katespade.com']

    base_url = 'https://eu.katespade.com/de-de'

    def start_requests(self):
        product_category = self.product_category
        for url in product_category.keys():
            meta = {
                "category_name": product_category.get(url),
                "referer": url,
            }
            request_url = url + "?format=page-element"
            yield scrapy.Request(request_url, meta=meta, callback=self.parse_product_list,
                                 errback=self.start_request_error)

    def parse_product_list(self, response):
        product_xpath = '//div[@class="product-tile"]'
        base_url_xpath = 'div[@class="product-name"]/a'
        color_xpath = 'div[@class="product-swatches"]/ul/li/a'
        next_page_xpath = '//a[@class="load-more-wrapper"]/@href'
        page_size = 30
        start = response.meta.get("start", 0)

        product_data = response.xpath(product_xpath)
        for item in product_data:
            if color_list := item.xpath(color_xpath):
                for data in color_list:
                    if url := data.attrib.get("href"):
                        item_data = {
                            "category_name": response.meta.get("category_name"),
                            "referer": response.meta.get("referer"),
                            "url": url,
                        }
                        yield ProductUrlItem(**item_data)
                        yield scrapy.Request(url, meta=response.meta, callback=self.parse_product_detail)

            else:
                url = item.xpath(base_url_xpath).attrib.get("href")
                if not url.startswith(self.base_url):
                    url = self.base_url + url

                item_data = {
                    "category_name": response.meta.get("category_name"),
                    "referer": response.meta.get("referer"),
                    "url": url,
                }
                yield ProductUrlItem(**item_data)

                yield scrapy.Request(url, meta=response.meta, callback=self.parse_product_detail)

        if response.xpath(next_page_xpath).get():
            start = start + len(product_data)
            response.meta['start'] = start
            next_href = response.meta.get("referer") + f"?start={start}&sz={page_size}&format=page-element"
            yield scrapy.Request(next_href, meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error)

    def parse_product_detail(self, response):

        image_xpath = '//li[@class="thumb "]/a'
        json_data_xpath = '//script[@type="application/ld+json"]'
        size_xpath = '//ul[@class="swatches size"]//a[@class="swatchanchor"]/text()'
        image_data = response.xpath(image_xpath)
        images = []

        for item in image_data:
            img = item.attrib.get("href")
            images.append(img)

        product_data = json.loads(response.xpath(json_data_xpath)[0].root.text.replace("\r", '').replace("\n", ''))
        size_list = response.xpath(size_xpath).getall()
        size_list = [data.strip() for data in size_list]
        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "category_name": response.meta.get("category_name"),
            "sku": product_data.get("sku"),
            "color": product_data.get("color"),
            "size": size_list,
            "img": images,
            "price": product_data.get("offers").get("price"),
            "title": product_data.get("name"),
            "dade": datetime.now(),
            "basc": product_data.get('description'),
            "brand": ""
        }
        yield ProductDetailItem(**item_data)
