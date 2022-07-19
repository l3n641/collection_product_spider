import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime
from urllib.parse import urlencode


class MangoSpider(CommonSpider):
    name = 'mango'
    allowed_domains = ['mango.com']
    headers = {
        "stock-id": "400.US.0.true.false.v1"
    }

    def parse_product_list(self, response):
        if response.url != response.meta.get("referer"):
            print(f"链接{response.meta.get('referer')}已经被重定向:{response.url}")
            yield scrapy.Request(response.meta.get('referer'), meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error, dont_filter=True)
            return False

        pattern = 'var viewObjectsJson = (.*);'
        data = response.selector.re(pattern)
        if not data:
            raise ValueError("获取分类js失败")

        js_data = json.loads(data[0])
        catalog_params = js_data.get('catalogParameters')
        if not catalog_params:
            raise ValueError(f"没有找到对应的链接:{response.url}")

        base_url = 'https://shop.mango.com/services/productlist/products'
        iso_code = catalog_params.get("isoCode")
        id_shop = catalog_params.get('idShop')
        id_section = catalog_params.get('idSection')
        family = catalog_params.get('family')
        id_sub_section = catalog_params.get('optionalParams').get("idSubSection")
        params = {
            "pageNum": 1,
            "rowsPerPage": 20,
            "columnsPerRow": 4,
            "family": family,
            "idSubSection": id_sub_section,
        }
        page_list_url = base_url + f'/{iso_code}/{id_shop}/{id_section}/?'
        response.meta["request_params"] = params
        response.meta["page_list_url"] = page_list_url
        params_str = urlencode(params)
        request_url = page_list_url + params_str

        yield scrapy.Request(request_url, meta=response.meta, callback=self.parse_product_list_2,
                             errback=self.start_request_error)

    def parse_product_list_2(self, response):
        data = response.json()

        for group in data.get("groups"):
            garments = group.get("garments")
            for _, item in garments.items():
                detail_url = f"https://shop.mango.com/services/garments/{item.get('id')}"

                item_data = {
                    "category_name": response.meta.get("category_name"),
                    "detail_url": detail_url,
                    "referer": response.meta.get("referer"),
                    "meta": response.meta,
                    "headers": self.headers,
                    "callback": self.parse_product_detail,
                    "page_url": response.url
                }
                for task in self.request_product_detail(**item_data):
                    yield task

        if not data.get("lastPage"):
            meta = response.meta.copy()
            request_params = meta.get("request_params")
            request_params["pageNum"] = request_params["pageNum"] + 1
            params_str = urlencode(request_params)
            request_url = response.meta.get("page_list_url") + params_str

            yield scrapy.Request(request_url, meta=response.meta, callback=self.parse_product_list_2,
                                 errback=self.start_request_error)

    def parse_product_detail(self, response):
        data = response.json()
        title = data.get("name")
        product_id = data.get("id")
        html_url = "https://shop.mango.com/" + data.get("canonicalUrl")
        default_size = []
        for item in data.get("colors").get("colors"):
            sku = product_id + "_" + item.get("id")
            price = item.get("price").get("price")
            sizes = self.get_size(item.get("sizes")) or default_size
            if not default_size and sizes:
                default_size = sizes

            if not item.get("images"):
                continue

            images = self.get_image(item.get("images"))
            product = data.get("dataLayer").get("ecommerce").get("detail").get("products")[0]
            item_data = {
                "project_name": self.project_name,
                "PageUrl": response.url,
                "html_url": html_url,
                "category_name": response.meta.get("category_name"),
                "sku": sku,
                "color": item.get("label"),
                "size": sizes,
                "img": images,
                "price": price,
                "title": title,
                "dade": datetime.now(),
                "basc": product.get("description"),
                "brand": product.get("brand")
            }
            yield ProductDetailItem(**item_data)

    @staticmethod
    def get_size(sizes):
        data = []
        if not sizes:
            return data
        for size_data in sizes:
            if size_data.get("id") == "-1":
                continue
            if size_data.get("label") in data:
                continue
            data.append(size_data.get("label"))
        return data

    @staticmethod
    def get_image(images):
        image_base_url = 'https://st.mngbcn.com/rcs/pics/static'

        data = []
        for item in images:
            for sub_item in item:
                data.append(image_base_url + sub_item.get("url"))

        return data

    def get_failed_quest_data(self, item, **kwargs):
        data = super(MangoSpider, self).get_failed_quest_data(item, headers=self.headers)
        return data
