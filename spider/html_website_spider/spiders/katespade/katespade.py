import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime
from urllib.parse import urlparse


class KatespadeSpider(CommonSpider):
    name = 'katespade'
    allowed_domains = ['katespade.com']

    base_url = 'https://www.katespade.com'

    def start_requests(self):
        product_category = self.product_category
        for url in product_category.keys():
            result = urlparse(url)
            request_url = self.base_url + result.path + ".json"

            meta = {
                "category_name": product_category.get(url),
                "referer": url,
                "request_url": request_url,
            }
            yield scrapy.Request(request_url, meta=meta, callback=self.parse_product_list,
                                 errback=self.start_request_error)

    def parse_product_list(self, response):
        if not urlparse(response.url).path.endswith(".json"):
            result = urlparse(response.url)
            request_url = self.base_url + result.path + ".json"
            yield scrapy.Request(request_url, meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error)
        else:
            try:
                response_json = response.json()
            except  Exception as e:
                print(response.url)
                return

            item_data = {
                "category_name": response.meta.get("category_name"),
                "url": response.url,
                "referer": response.meta.get("referer"),
            }
            yield ProductUrlItem(**item_data)

            subcategory = response_json.get('subcategory')
            start = response.meta.get("start", 0)

            if subcategory and (items := subcategory.get("items")):
                total_record = subcategory.get("total")
                if total_record > start + len(items):
                    next_start = start + len(items)
                    meta = {
                        "category_name": response.meta.get("category_name"),
                        "referer": response.meta.get("referer"),
                        "request_url": response.meta.get("request_url"),
                        "start": next_start,
                    }
                    request_url = response.meta.get("request_url") + f"?start={next_start}&sz=12"
                    yield scrapy.Request(request_url, meta=meta, callback=self.parse_product_list,
                                         errback=self.start_request_error)

                for item in items:
                    meta = {
                        "category_name": response.meta.get("category_name"),
                    }

                    if options := item.get("color").get("options"):
                        for option in options:
                            request_url = self.base_url + option.get("url")
                            yield scrapy.Request(request_url, meta=meta, callback=self.parse_product_detail)

                    else:
                        request_url = self.base_url + item.get("url")
                        yield scrapy.Request(request_url, meta=meta, callback=self.parse_product_detail)

    def parse_product_detail(self, response):

        image_xpath = '//div[contains(@class,"product-thumbnails-list")]//img'
        json_data_xpath = '//script[@type="application/ld+json"]'
        size_xpath = '//div[@data-availablesizes]'
        id_xpath = '//input[@name="id"]/@value'
        product_id = response.xpath(id_xpath).get() or ""
        image_data = response.xpath(image_xpath)
        images = []

        for item in image_data:
            img = item.attrib.get("src").replace("$s7productThumbnail$", "$s7fullsize$")
            images.append(img)

        product_data = json.loads(response.xpath(json_data_xpath)[0].root.text.replace("\r", '').replace("\n", ''))
        size_list = response.xpath(size_xpath).attrib.get('data-availablesizes').split(":")
        size_list = [data.strip() for data in size_list]
        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "category_name": response.meta.get("category_name"),
            "sku": product_id + "_" + product_data.get("sku") if product_id else product_data.get("sku"),
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
