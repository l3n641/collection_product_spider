import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime


class PullandbearSpider(CommonSpider):
    name = 'pullandbear'
    allowed_domains = ['pullandbear.com']

    category_url = 'https://www.pullandbear.com/itxrest/3/catalog/store/24009477/20309434/category/{}/product?languageId=-15&showProducts=false&appId=1'
    product_detail_url = "https://www.pullandbear.com/itxrest/2/catalog/store/24009477/20309434/category/0/product/{}/detail?languageId=-15&appId=1"

    def parse_product_list(self, response, **kwargs):
        pattern = 'inditex.iCategoryId = (.*);'
        data = response.selector.re_first(pattern)
        url = self.category_url.format(data.strip())
        yield scrapy.Request(url=url, meta=response.meta, callback=self.parse_product_list_2,
                             errback=self.start_request_error)

    def parse_product_list_2(self, response):
        data = response.json()
        product_ids = data.get("productIds")
        for product_id in product_ids:
            url = self.product_detail_url.format(product_id)
            item_data = {
                "category_name": response.meta.get("category_name"),
                "url": url,
                "referer": response.meta.get("referer"),
            }
            yield ProductUrlItem(**item_data)
            yield scrapy.Request(url=url, meta=response.meta, callback=self.parse_product_detail)

    def parse_product_detail(self, response, **kwargs):
        data = response.json()
        product_id = data.get('id')
        description = data.get("detail").get('longDescription')
        title = data.get("name")

        for item in data.get("bundleProductSummaries"):
            detail = item.get("detail")
            xmedia = detail.get('xmedia')

            for item in detail.get("colors"):
                sku = f"{product_id}_{item.get('id')}"
                size_list = []
                price = None
                for size in item.get("sizes"):
                    price = int(size.get("price")) / 100
                    size_list.append(size.get("name"))

                images = self.get_img(item.get("id"), xmedia)
                item_data = {
                    "project_name": self.project_name,
                    "PageUrl": response.url,
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
        base_url = "https://static.pullandbear.net/2/photos"
        for data in media:
            if data.get("colorCode") == color_code:
                path = data.get("path")

                xmedia_locations = data.get("xmediaLocations")
                if not xmedia_locations:
                    return images

                locations = xmedia_locations[0].get("locations")
                if locations and len(locations) > 1 and (media_locations := locations[1].get("mediaLocations")):
                    for file in media_locations:
                        url = f"{base_url}{path}/{file}8.jpg?imwidth=1280"
                        images.append(url)
                return images
