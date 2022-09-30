import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime
import requests
import re
from urllib.parse import urlparse, urljoin


class TriplefatgooseSpider(CommonSpider):
    name = 'triplefatgoose'
    allowed_domains = ['triplefatgoose.com', "mybcapps.com"]

    def parse_product_list(self, response, **kwargs):
        url_xpath = '//h3[@class="card__heading"]/a'
        data = response.xpath(url_xpath)
        for item in data:
            detail_url = response.meta.get("referer") + item.attrib.get("href")
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
        if data:
            next_page = response.meta.get("page", 1) + 1
            url = response.meta.get("referer") + f"?page={next_page}"
            response.meta["page"] = next_page
            yield scrapy.Request(url, meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error, dont_filter=True)

    def parse_product_detail(self, response):
        colors_xpath = '//variant-radios/fieldset/input[@name="Color"]'
        size_xpath = '//variant-radios/fieldset/input[@name="Size"]'
        meta_data_xpath = '//script[@type="application/ld+json"]/text()'
        product_id = response.selector.re_first("ProductID: (.*?),")
        title = response.selector.re_first('Name: "(.*?)",')
        price_xpath = '//meta[@property="og:price:amount"]'
        price = response.xpath(price_xpath).attrib.get("content")
        meta_data = json.loads(response.xpath(meta_data_xpath).get())
        sizes = []
        for item in response.xpath(size_xpath):
            sizes.append(item.attrib.get("value"))

        for item in response.xpath(colors_xpath):
            color = item.attrib.get("value").lower()
            images = []
            sku = product_id + "_" + color.replace(" ", "-")
            image_xpath = f'//ul[@role="list"]/li[@data-alt="{color}"]//img'
            for image_node in response.xpath(image_xpath):
                src = "https:" + image_node.attrib.get("src")
                url = urljoin(src, urlparse(src).path)
                images.append(url)
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
                "basc": meta_data.get("description"),
                "brand": meta_data.get("brand").get("name")
            }

            yield ProductDetailItem(**item_data)
