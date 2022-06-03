# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import ProductUrlItem
from .models import ProductUrl
from . import Session


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
