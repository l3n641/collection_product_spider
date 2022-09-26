import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime


class OyshoSpider(CommonSpider):
    name = 'oysho'
    allowed_domains = ['oysho.com']

    category_url = 'https://www.oysho.com/itxrest/3/catalog/store/64009677/60361120/category/{}/product?languageId=-1&appId=1&showProducts=false'
    product_detail_url = "https://www.oysho.com/itxrest/2/catalog/store/64009677/60361120/category/0/product/{}/detail?languageId=-1&appId=1"

    def parse_product_list(self, response, **kwargs):
        pattern = 'iCategoryId:(.*),'
        data = response.selector.re_first(pattern)
        url = self.category_url.format(data.strip())
        yield scrapy.Request(url=url, meta=response.meta, callback=self.parse_product_list_2,
                             errback=self.start_request_error)

    def parse_product_list_2(self, response):
        data = response.json()
        product_ids = data.get("productIds")
        for product_id in product_ids:
            detail_url = self.product_detail_url.format(product_id)

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

    def parse_product_detail(self, response, ):
        data = response.json()
        product_id = data.get('id')
        description = data.get("detail").get('longDescription')
        title = data.get("name")
        color_id = data.get("mainColorid")
        if not data.get("bundleProductSummaries"):
            return None
        bundle_product_summaries = data.get("bundleProductSummaries")[0]
        detail = bundle_product_summaries.get("detail")
        xmedia = detail.get('xmedia')
        sku = f"{product_id}_{color_id}"
        html_url = data.get("productUrl")
        for item in detail.get("colors"):
            if item.get("id") != color_id:
                continue
            size_list = []
            price = None
            for size in item.get("sizes"):
                price = int(size.get("price", 0)) / 100
                size_list.append(size.get("name"))

            images = self.get_img(item.get("id"), xmedia)
            item_data = {
                "project_name": self.project_name,
                "PageUrl": response.url,
                "html_url": html_url,
                "category_name": response.meta.get("category_name"),
                "sku": sku,
                "color": item.get("name"),
                "size": size_list,
                "img": images,
                "price": price,
                "title": title,
                "dade": datetime.now(),
                "basc": description,
                "brand": ""
            }

            yield ProductDetailItem(**item_data)

    @staticmethod
    def get_img(color_code: str, media: list):
        images = []
        base_url = "https://static.oysho.net/6/photos2"
        for data in media:
            if data.get("colorCode") == color_code:
                path = data.get("path")

                xmedia_locations = data.get("xmediaLocations")
                if not xmedia_locations:
                    return images

                locations = xmedia_locations[0].get("locations")
                if locations and len(locations) > 1 and (media_locations := locations[1].get("mediaLocations")):
                    for file in media_locations:
                        url = f"{base_url}{path}/{file}0.jpg?imwidth=1011"
                        images.append(url)
                return images

    def start_requests_te(self):
        url = "https://www.oysho.com/itxrest/2/catalog/store/64009677/60361120/category/1010277516/product/114222637/detail?languageId=-1&appId=1"
        yield scrapy.Request(url, callback=self.parse_product_detail)
