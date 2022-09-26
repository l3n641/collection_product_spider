import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode


class LowesSpider(CommonSpider):
    name = 'lowes'
    allowed_domains = ['lowes.com']
    base_url = 'https://www.lowes.com'

    headers = {
        "Accept": "*/*",
        "User-Agent": "PostmanRuntime/7.29.0",
        'Connection': 'keep-alive',
        "Accept-Encoding": "gzip, deflate, br",
    }

    def start_requests(self):
        product_category = self.product_category
        for url in product_category.keys():

            result = urlparse(url)
            params = parse_qs(result.query)
            catalog = ''
            refinement = ''
            if params.get('catalog'):
                catalog = params.get('catalog')[0]

            if params.get('refinement'):
                refinement = params.get('refinement')[0]

            args = {
                "facets": refinement if refinement else catalog,
                "nearByStores": '2211,1895,1756,1132,2273',
                "minimumMatch": '',
            }

            request_url = self.base_url + result.path + "/products?" + urlencode(args)
            meta = {
                "category_name": product_category.get(url),
                "referer": url,
                "request_url": request_url,
            }
            yield scrapy.Request(request_url, meta=meta, callback=self.parse_product_list,
                                 errback=self.start_request_error, headers=self.headers, )

    def parse_product_list(self, response):

        data = response.json()

        if (pagination := data.get('pagination')) and pagination.get("page") < pagination.get("pageCount"):
            next_page_url = response.meta["request_url"] + "&" + urlencode({"page": pagination.get("page") + 1})
            yield scrapy.Request(next_page_url, meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error, headers=self.headers)

        item_list = data.get("itemList")
        for item in item_list:
            product = item.get("product")
            product_id = product.get("omniItemId")
            detail_url = f"https://www.lowes.com/pd/{product_id}/productdetail/2790/Guest"

            item_data = {
                "category_name": response.meta.get("category_name"),
                "referer": response.meta.get("referer"),
                "url": detail_url,
            }
            yield ProductUrlItem(**item_data)

            yield scrapy.Request(detail_url, meta=response.meta, callback=self.parse_product_detail,
                                 headers=self.headers)

    def parse_product_detail(self, response, **kwargs):
        data = response.json()
        sku = data.get("productId")
        product_detail = data.get("productDetails").get(sku)
        product = product_detail.get("product")
        if product_detail.get("price"):
            price = product_detail.get("price").get("analyticsData").get("sellingPrice")

            images = []
            image_urls = product.get("imageUrls")
            image_base_url = 'https://mobileimages.lowes.com/';
            for item in image_urls:
                if item.get("key") == 'baseUrl':
                    image_src = image_base_url + item.get("value") + "?size=pdhism"
                    images.append(image_src)

            if product.get("epc"):
                extra_images = product.get("epc").get("additionalImages", [])
                for item in extra_images:
                    images.append(item.get("baseUrl") + "?size=pdhism")
            brand = product.get("brand")
            item_data = {
                "project_name": self.project_name,
                "PageUrl": response.url,
                "category_name": response.meta.get("category_name"),
                "sku": sku,
                "color": "",
                "size": [],
                "img": images,
                "price": price,
                "title": product.get("title"),
                "dade": datetime.now(),
                "basc": product.get("romanceCopy"),
                "brand": brand
            }
            yield ProductDetailItem(**item_data)
