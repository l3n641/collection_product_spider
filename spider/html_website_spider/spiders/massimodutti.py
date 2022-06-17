import json
import scrapy
from ..items import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from .common_spider import CommonSpider


class Massimodutti(CommonSpider):
    name = 'massimodutti'
    allowed_domains = ['www.massimodutti.com']
    BASE_URL = "https://www.massimodutti.com/"
    detail_api_url = 'https://www.massimodutti.com/itxrest/2/catalog/store/34009456/30359502/category/0/product/{}/detail?languageId=-1&appId=1'

    def parse_product_list(self, response, **kwargs):
        pattern = '<li><a href="(.*?)"><img'
        data = response.selector.re(pattern)
        category_name = response.meta.get("category_name")
        meta = {"category_name": category_name}
        for url in data:
            item_data = {
                "category_name": category_name,
                "url": url,
                "referer": response.url,
            }
            yield ProductUrlItem(**item_data)

            yield scrapy.Request(url=url, meta=meta, callback=self.parse_product_detail)

    def parse_product_detail(self, response, **kwargs):
        pattern = "inditex.iProductId = (\d+);"
        product_id = response.selector.re_first(pattern)
        detail_api_url = self.detail_api_url.format(product_id)
        if product_id:
            response.meta['url'] = response.url
            yield scrapy.Request(url=detail_api_url, meta=response.meta, callback=self.parse_product_extra_data)
        else:
            error_msg = f"链接没有找到对应的详情{response.url}"
            print(error_msg)

    def parse_product_extra_data(self, response, **kwargs):
        data = response.json()
        product_id = data.get('id')
        detail = data.get("detail")
        description = ""
        for item in data.get("attributes"):
            if item.get("type") == "DESCRIPTION":
                description = description + " " + item.get("value")

        xmedia = detail.get("xmedia")
        title = data.get("name")

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
                "PageUrl": response.meta.get("url"),
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
        base_url = "https://static.massimodutti.net/3/photos"
        for data in media:
            if data.get("colorCode") == color_code:
                path = data.get("path")

                file_data = data.get("xmediaLocations")[0].get("locations")[1].get("mediaLocations")
                for file in file_data:
                    url = f"{base_url}{path}/{file}16.jpg?imwidth=700"
                    images.append(url)
                return images
