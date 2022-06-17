import json
import scrapy
from ..items import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from .common_spider import CommonSpider
from scrapy.http import JsonRequest
import math


class CASpider(CommonSpider):
    name = 'ca'
    allowed_domains = ['www.c-and-a.com']
    BASE_URL = "https://www.c-and-a.com"

    def parse_product_list(self, response, **kwargs):
        meta_xpath = '//meta[@name="canda-appdeeplink"]'
        url = "https://www.c-and-a.com/api?o=list"
        category_name = response.meta.get("category_name")
        headers = {
            "origin": "https://www.c-and-a.com",
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",

        }
        content = response.xpath(meta_xpath).attrib.get("content")
        if content and (res := content.split("=")) and len(res) == 2:
            category_id = res[1]
            post_data = self.get_post_data(category_id)
            meta = {"category_name": category_name}
            yield JsonRequest(url, method="POST", data=post_data, meta=meta, callback=self.parse_se_product_list,
                              headers=headers)
        else:
            msg = f"{response.url} 没有对应的分类id"
            print(msg)

    @staticmethod
    def get_post_data(category_id, page=1):
        post_data = {
            "operationName": "list",
            "variables": {
                "page": page,
                "id": f"{category_id}",
                "fetchNavigation": False
            },
            "query": "query list($id: ID!, $page: Int, $sorting: Int, $filter: [ListFilterFacet!], $fetchNavigation: Boolean!) {\n  list(id: $id, page: $page, sorting: $sorting, filter: $filter) {\n    id\n    page\n    productCount\n    navigation @include(if: $fetchNavigation) {\n      ...ListNavigation\n      __typename\n    }\n    products {\n      ...ListProduct\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Image on Image {\n  url\n  file\n  folder\n  __typename\n}\n\nfragment ListNavigation on ListNavigation {\n  parent {\n    id\n    name\n    productCount\n    slug\n    __typename\n  }\n  current {\n    id\n    name\n    __typename\n  }\n  children {\n    id\n    name\n    productCount\n    slug\n    __typename\n  }\n  __typename\n}\n\nfragment ListProductVariant on ProductVariant {\n  wcsId\n  uri\n  isAvailable\n  modelImage {\n    ...Image\n    __typename\n  }\n  variantImage {\n    ...Image\n    __typename\n  }\n  sizes {\n    wcsId\n    label\n    available\n    isAvailable\n    itemUsim\n    __typename\n  }\n  color {\n    colorCode\n    label\n    image {\n      ...Image\n      __typename\n    }\n    __typename\n  }\n  price {\n    strikePrice\n    grossPriceFormatted\n    strikePriceFormatted\n    discountFlag\n    __typename\n  }\n  __typename\n}\n\nfragment ListProduct on ListProduct {\n  usim\n  uri\n  name\n  collectionLabel\n  flag\n  isSustainable\n  prudsysTrackingToken\n  variants {\n    ...ListProductVariant\n    __typename\n  }\n  variantCount\n  tracking {\n    id\n    price\n    color\n    viewIDs\n    sizes\n    sizesAvailable\n    sale\n    __typename\n  }\n  __typename\n}"
        }
        return post_data

    def parse_se_product_list(self, response, **kwargs):
        page_size = 60

        data = response.json()
        info = data.get("data").get("list")
        products = info.get("products")
        for product in products:
            variant = product.get("variants")[0]
            tracking = product.get("tracking")
            url = self.BASE_URL + product.get("uri")
            sku = product.get("usim") + "_" + variant.get("wcsId")
            size = tracking.get("sizes")
            meta = {
                "category_name": response.meta.get("category_name"),
                "size": size,
                "sku": sku,
                "price": tracking.get("price"),
            }
            yield scrapy.Request(url, meta=meta, callback=self.parse_product_detail)

    def parse_product_detail(self, response, **kwargs):
        color_xpath = '//span[@data-qa="ProductDetailColorsLabel"]/text()'
        title_xpath = '//h1[@data-qa="ProductName"]/text()'
        desc_xpath = '//meta[@name="description"]'
        image_base_url = 'https://www.c-and-a.com/img/product/q_auto:good,b_rgb:E0DEDA,c_scale,w_574/'
        images = []
        try:
            image_data_list = json.loads(response.selector.re_first('\\"images.*?:(.*?]),').replace("\\", ''))
            for data in image_data_list:
                prefix, file = data.get("file").split("/")
                url = image_base_url + f"{prefix}{data.get('folder')}/{file}"
                images.append(url)
        except Exception:
            print("加载图片失败")

        item = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "category_name": response.meta.get("category_name"),
            "sku": response.meta.get("sku"),
            "color": response.xpath(color_xpath).get(),
            "size": response.meta.get("size"),
            "img": images,
            "price": response.meta.get("price"),
            "title": response.xpath(title_xpath).get(),
            "dade": datetime.now(),
            "basc": response.xpath(desc_xpath).attrib.get("content"),
            "brand": '',
        }
        yield ProductDetailItem(**item)
