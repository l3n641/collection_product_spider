import scrapy
from ..common_spider import CommonSpider
from .. import ProductDetailItem
import json
from datetime import datetime
from urllib.parse import urlencode


class BackcountrySpider(CommonSpider):
    name = 'backcountry'
    allowed_domains = ['backcountry.com']
    base_url = "https://www.backcountry.com"

    def parse_product_list(self, response, **kwargs):
        category_xpath = '//script[@type="application/json"]/text()'
        category_data = json.loads(response.xpath(category_xpath).get())
        page_props = category_data.get("props").get('pageProps')
        query = page_props.get('query')
        query['page'] = 0
        api_url = self.base_url + page_props.get('baseUrl')

        response.meta["query"] = query
        response.meta["api_url"] = api_url

        detail_url = api_url + "?" + urlencode(query)
        yield scrapy.Request(detail_url, meta=response.meta, callback=self.parse_product_list2,
                             errback=self.start_request_error,
                             dont_filter=True)

    def parse_product_list2(self, response):
        json_data = response.json()
        for item in json_data.get("products"):
            detail_url = self.base_url + item.get("url")
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

        query = response.meta.get('query')
        page = query.get("page")
        current = (page + 1) * 42
        if current < json_data.get("metadata").get("found"):
            meta = response.meta.copy()
            query['page'] = query['page'] + 1
            api_url = meta.get('api_url')
            meta["query"] = query
            detail_url = api_url + "?" + urlencode(query)
            yield scrapy.Request(detail_url, meta=meta, callback=self.parse_product_list2,
                                 errback=self.start_request_error,
                                 dont_filter=True)

    def parse_product_detail(self, response):
        data_xpath = '//script[@type="application/json"]/text()'
        product_data = json.loads(response.xpath(data_xpath).get())
        page_props = product_data.get("props").get('pageProps')
        product = page_props.get("product")
        title = product.get("title")
        size = []
        for data in product.get("sizesCollection"):
            size.append(data)
        _id = product.get("id")
        brand = product.get("brand").get("name")
        price = product.get("activePrice").get("minSalePrice")
        description = page_props.get("metadata").get("ogDescription") or page_props.get("metadata").get(
            "defaultDescription")
        selected_color = product.get("selectedColor")
        for key in product.get("colorsCollection"):
            if key != selected_color:
                continue
            item = product.get("colorsCollection").get(key)
            color = item.get("name")
            color_id = item.get("id")
            sku = _id + "_" + color_id
            images = [self.base_url + item.get("twelveHundredImg")]
            images = images + self.get_extra_images(color_id, product.get("detailImages"))
            item_data = {
                "project_name": self.project_name,
                "PageUrl": response.url,
                "html_url": response.url,
                "category_name": response.meta.get("category_name"),
                "sku": sku,
                "color": color,
                "size": size,
                "img": images,
                "price": price,
                "title": title,
                "dade": datetime.now(),
                "basc": description,
                "brand": brand
            }

            yield ProductDetailItem(**item_data)

    def get_extra_images(self, color_id, detail_images):
        images = []
        for data in detail_images:
            if color_id in data.get("colors"):
                images.append(self.base_url + data.get("twelveHundredImg"))

        return images
