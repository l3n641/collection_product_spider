import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime


class ZaraSpider(CommonSpider):
    name = 'zara'
    allowed_domains = ['www.zara.com']

    base_url = 'https://www.zara.com/uk/en'
    category_url = 'https://www.zara.com/uk/en/categories?ajax=true'

    def start_requests(self):
        yield scrapy.Request(self.category_url, callback=self.parse_category_list)

    def parse_category_list(self, response, **kwargs):
        # 收集category id
        data_json = response.json()
        seo_category_dict = {}
        for parent_category in data_json.get("categories"):
            category = self.get_sub_category(parent_category)
            seo_category_dict.update(category)

        for url in self.product_category:
            category_id = self.get_cid_by_seo_category_id(url, seo_category_dict)
            if not category_id:
                print(f"基础链接没有找到：{url}")
                continue
            meta = {"category_name": self.product_category.get(url), "category_id": category_id}
            requests_url = f"{self.base_url}/category/{category_id}/products?ajax=true"
            yield scrapy.Request(requests_url, callback=self.parse_product_list, meta=meta)

    @classmethod
    def get_sub_category(cls, parent_category: list):
        category_dict = {}
        for sub_category in parent_category.get("subcategories"):
            if not sub_category.get("seo"):
                continue
            seo_id = sub_category.get("seo").get("seoCategoryId")
            category_dict[seo_id] = sub_category.get("id")
            if sub_category.get("subcategories"):
                child_category = cls.get_sub_category(sub_category)
                category_dict.update(child_category)

        return category_dict

    @staticmethod
    def get_cid_by_seo_category_id(url: str, seo_category_dict: dict):
        for seo_category_id in seo_category_dict:
            if url.endswith(f"{seo_category_id}.html"):
                return seo_category_dict.get(seo_category_id)

    def parse_product_list(self, response, **kwargs):
        data = response.json()
        category_id = response.meta.get("category_id")
        category_name = response.meta.get("category_name")

        product_groups = data.get('productGroups')
        for item in product_groups:
            products = item.get('elements')
            for product in products:
                if not product.get('commercialComponents'):
                    continue
                for commercial in product.get('commercialComponents'):
                    seo_data = commercial.get("seo")
                    if not commercial.get("detail"):
                        continue
                    colors = commercial.get("detail").get("colors")
                    url = f"{self.base_url}/{seo_data.get('keyword')}-p{seo_data.get('seoProductId')}.html?v1={seo_data.get('discernProductId')}&v2={category_id}"
                    item_data = {
                        "category_name": category_name,
                        "url": url,
                        "referer": response.url,
                    }
                    try:
                        yield ProductUrlItem(**item_data)
                    except Exception as e:
                        print(e)
                    else:
                        meta = {
                            "category_id": category_id,
                            "category_name": category_name,
                            "color": colors[0].get("name") if colors else ''
                        }
                        yield scrapy.Request(url, callback=self.parse_product_detail, meta=meta)

    def parse_product_detail(self, response, **kwargs):
        product_data_xpath = '//script[@type="application/ld+json"]'
        size_xpath = '//span[@class="product-detail-size-info__main-label"]'
        if not response.xpath(product_data_xpath):
            return False

        product_data = json.loads(response.xpath(product_data_xpath)[0].root.text)
        if not product_data:
            return False

        first_product = product_data[0]

        size_data = response.xpath(size_xpath)
        size = []
        if size_data:
            for item in size_data:
                if item.root.text:
                    size.append(item.root.text)
        images = []
        for image in first_product.get('image'):
            images.append(image.replace("w/1920", "w/1280"))

        item = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "category_name": response.meta.get("category_name"),
            "sku": first_product.get("sku"),
            "color": response.meta.get("color"),
            "size": size,
            "img": images,
            "price": first_product.get('offers').get("price"),
            "title": first_product.get("name"),
            "dade": datetime.now(),
            "basc": first_product.get("description"),
            "brand": first_product.get("brand"),
        }
        yield ProductDetailItem(**item)
