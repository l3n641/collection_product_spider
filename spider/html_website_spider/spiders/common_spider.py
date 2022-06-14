from spider.html_website_spider.libs.product_excel import ProductExcel
from spider.html_website_spider.models import Base
from spider.html_website_spider.libs.sqlite import Sqlite
from scrapy.utils.project import get_project_settings
import os
import scrapy


class CommonSpider(scrapy.Spider):

    def __init__(self, category_file_path=None, *args, **kwargs):
        if not os.path.exists(category_file_path):
            raise ValueError("产品类别文件不存在")

        project_settings = get_project_settings()
        file = ProductExcel(category_file_path)
        product_category = file.get_category()
        self.product_category = product_category

        db_engine = Sqlite.get_sqlite_engine(file.project_name, project_settings.get("DB_DIR_PATH"))
        Sqlite.set_session_class(db_engine)
        Base.metadata.create_all(db_engine)

        super(CommonSpider).__init__(*args, **kwargs)

    def start_requests(self):
        product_category = self.product_category
        for url in product_category.keys():
            meta = {
                "category_name": product_category.get(url)
            }
            yield scrapy.Request(url, meta=meta, callback=self.parse_product_list)
