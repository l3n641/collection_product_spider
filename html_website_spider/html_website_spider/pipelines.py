# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import ProductUrlItem, ProductDetailItem
from .models import ProductUrl, ProductDetail
from . import Session
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class ProductUrlPipeline:
    def open_spider(self, spider):
        session = Session()
        self.session = session

    def process_item(self, item, spider):
        if not isinstance(item, ProductUrlItem):
            return item

        model = ProductUrl(url=item.get("url"), category_name=item.get("category_name"), referer=item.get("referer"))
        self.session.add(model)
        self.session.commit()


class ImageDownloadPipeline(ImagesPipeline):

    def open_spider(self, spider):
        super(ImageDownloadPipeline, self).open_spider(spider)
        session = Session()
        self.session = session

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
        data = {
            "PageUrl": item.get("PageUrl"),
            "category_name": item.get("category_name"),
            "sku": item.get("sku"),
            "color": item.get("color"),
            "size": size,
            "img": img,
            "price": item.get("price"),
            "title": item.get("title"),
            "dade": item.get("dade"),
            "basc": item.get("basc"),
            "brand": item.get("brand"),
        }
        model = ProductDetail(**data)
        self.session.add(model)
        self.session.commit()
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = request.meta.get("img_id")
        return f'{item.get("sku")}/{image_guid}.jpg'
