# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import ProductUrlItem, ProductDetailItem
from .models import ProductUrl, ProductDetail, DownloadImageLog
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from .libs.sqlite import Sqlite
from io import BytesIO


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
        success_files = []
        session = Sqlite.get_session()
        image_paths = []
        for status, detail in results:
            if status:
                success_files.append(detail.get("url"))
                local_path = detail["path"]
                image_paths.append(f'<img src="{local_path}"/>')
                log = {
                    "sku": item.get("sku"),
                    "url": detail.get("url"),
                    "status": 1,
                    "local_path": local_path,
                }
                log_model = DownloadImageLog(**log)
                session.add(log_model)

        # 记录下载失败的图片
        for url in item.get("img", []):
            if url not in success_files:
                log = {
                    "sku": item.get("sku"),
                    "url": url,
                    "status": 0,
                }
                log_model = DownloadImageLog(**log)
                session.add(log_model)

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
            "html_url": item.get("html_url"),
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
        session.add(model)
        session.query(ProductUrl).filter(ProductUrl.url == item.get("PageUrl")).update({"status": 1})
        session.commit()
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = request.meta.get("img_id")
        return f'{item.get("project_name")}/{item.get("sku")}/{image_guid}.jpg'

    def convert_image(self, image, size=None):
        if (image.format == 'PNG' or image.format == 'WEBP') and image.mode == 'RGBA':
            background = self._Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode == 'P':
            image = image.convert("RGBA")
            background = self._Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        if size:
            image = image.copy()
            image.thumbnail(size, self._Image.ANTIALIAS)

        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
