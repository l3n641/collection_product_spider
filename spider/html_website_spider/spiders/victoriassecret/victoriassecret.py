import json

import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
from html import unescape
from urllib.parse import urlencode
from datetime import datetime
import demjson
from urllib.parse import urlparse, parse_qsl


class VictoriaSsecretSpider(CommonSpider):
    name = 'victoriassecret'
    allowed_domains = ['victoriassecret.com']
    base_url = "https://www.victoriassecret.com"

    custom_settings = {
        "CONCURRENT_REQUESTS": 4,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
    }

    stock_id = "ebc4bc64-3a03-4135-a0c8-762514701b9f"
    product_list_api = "https://api.victoriassecret.com/stacks/v23/"
    active_country = "us"

    def start_by_product_category(self):
        """
        从产品分类里爬取数据
        :return:
        """
        product_category = self.product_category
        for url in product_category.keys():
            meta = {
                "category_name": product_category.get(url),
                "referer": url,

            }
            yield scrapy.Request(url, meta=meta, callback=self.parse_product_list, errback=self.start_request_error,
                                 dont_filter=True, headers=self.default_headers)

    def parse_product_list(self, response, **kwargs):
        product_data_xpath = '//div[@type="application/json"]/text()'

        data_str = response.xpath(product_data_xpath).get()
        data = json.loads(data_str)

        for item in data:
            if collection_stacks := item.get("collectionStacks"):
                url_info = urlparse(collection_stacks.get("path"))
                query = dict(parse_qsl(url_info.query))
                # ?brand=vs&collectionId=c7a41272-69c9-4233-88f1-b76770be9149&maxSwatches=8&isPersonalized=true&activeCountry=US&cid=&platform=web&deviceType=&platformType=&perzConsent=true&tntId=80c18cf7-e198-4954-b195-6d14075ebfe6.34_0&screenWidth=1920&screenHeight=1080
                new_params = {
                    "offset": 0,
                    "limit": 180,
                    "maxSwatches": 8,
                    "isPersonalized": "true",
                    "collectionId": query.get("collectionId"),
                    "activeCountry": self.active_country,
                    "stackId": self.stock_id,
                }
                params = urlencode(new_params)
                url = self.product_list_api + f"?{params}"

        yield scrapy.Request(url, meta=response.meta, callback=self.parse_product_list2,
                             errback=self.start_request_error)

    def parse_product_list2(self, response, **kwargs):
        data = response.json()

        for item in data.get("stacks")[0].get("list"):

            detail_url = item.attrib.get("href")
            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": detail_url,
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "headers": self.default_headers,
                "callback": self.parse_product_detail,
            }

            for task in self.request_product_detail(**item_data):
                yield task

    def parse_product_detail(self, response):
        color_id_xpath = '//div[@id="swatchDropdown"]//button[@ data-articlecode]'
        product_info_xpath = '//div[@class="product parbase"]/script/text()'
        js_str = response.xpath(product_info_xpath).get().replace("var productArticleDetails = ", "").strip().strip(";")
        product_data = demjson.decode(js_str)
        product_nodes = response.xpath(color_id_xpath)
        for item in product_nodes:
            product_id = item.attrib.get("data-articlecode")
            article_code = product_data.get('articleCode')
            if data := product_data.get(product_id):
                sku = article_code + "_" + product_id
                title = data.get("title")
                color = data.get("name")
                desc = data.get('description')
                html_url = data.get('pdpLink')
                price = data.get('priceValue') or data.get('priceSaleValue')
                sizes = []
                if data.get('variants'):
                    for size in data.get('variants'):
                        sizes.append(size.get('sizeName'))
                images = []
                if data.get('vAssets'):
                    for img in data.get('vAssets'):
                        images.append("https:" + img.get('zoom'))

                item_data = {
                    "project_name": self.project_name,
                    "PageUrl": response.url,
                    "html_url": html_url,
                    "category_name": response.meta.get("category_name"),
                    "sku": sku,
                    "color": color,
                    "size": sizes,
                    "img": images,
                    "price": price,
                    "title": title,
                    "dade": datetime.now(),
                    "basc": desc,
                    "brand": product_data.get("brand")
                }

                yield ProductDetailItem(**item_data)

    def start_requests(self):

        url = 'https://www.stories.com/en/clothing/dresses/maxi-dresses/product.smocked-strappy-maxi-dress-black.1102894001.html'
        yield scrapy.Request(url, callback=self.parse_product_detail, errback=self.start_request_error,
                             dont_filter=True)
