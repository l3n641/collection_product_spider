# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import ProductUrlItem, ProductDetailItem
from .models import ProductUrl, ProductDetail
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from .libs.sqlite import Sqlite


class ProductUrlPipeline:

    def process_item(self, item, spider):
        if not isinstance(item, ProductUrlItem):
            return item

        session = Sqlite.get_session()

        model = ProductUrl(url=item.get("url"), category_name=item.get("category_name"), referer=item.get("referer"))
        session.add(model)
        session.commit()


class ProductDetailPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if not isinstance(item, ProductDetailItem):
            return item

        img_id = 1
        for image_url in item['img']:
            yield Request(image_url, meta={"img_id": img_id})
            img_id = img_id + 1

    def item_completed(self, results, item, info):
        if not isinstance(item, ProductDetailItem):
            return item

        image_paths = [f'<img src="{x["path"]}"/>' for ok, x in results if ok]

        img = '|'.join(image_paths)
        size = '|'.join(item.get("size")) if item.get("size") else None

        try:
            if item.get("price"):
                price = float(item.get("price"))
            else:
                price = 0
        except Exception as e:
            price = 0

        data = {
            "PageUrl": item.get("PageUrl"),
            "category_name": item.get("category_name"),
            "sku": item.get("sku"),
            "color": item.get("color"),
            "size": size,
            "img": img,
            "price": price,
            "title": item.get("title"),
            "dade": item.get("dade"),
            "basc": item.get("basc"),
            "brand": item.get("brand"),
        }
        model = ProductDetail(**data)
        session = Sqlite.get_session()

        session.add(model)
        session.commit()
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = request.meta.get("img_id")
        return f'{item.get("project_name")}/{item.get("sku")}/{image_guid}.jpg'
