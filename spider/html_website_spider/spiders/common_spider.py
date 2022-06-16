from ..libs.product_excel import ProductExcel
from ..models import Base
from ..libs.sqlite import Sqlite
from scrapy.utils.project import get_project_settings
import os
import scrapy


class CommonSpider(scrapy.Spider):
    project_name = None

    def __init__(self, category_file=None, *args, **kwargs):

        super(CommonSpider).__init__(*args, **kwargs)

        project_settings = get_project_settings()
        category_file_path = os.path.join(project_settings.get("PROJECT_STORE"), category_file)

        if not os.path.exists(category_file_path):
            raise ValueError("产品类别文件不存在")

        file = ProductExcel(category_file_path)
        product_category = file.get_category()
        self.product_category = product_category
        self.project_name = file.project_name

        db_engine = Sqlite.get_sqlite_engine(file.project_name, project_settings.get("DB_DIR_PATH"))
        Sqlite.set_session_class(db_engine)
        Base.metadata.create_all(db_engine)

    def start_requests(self):
        product_category = self.product_category
        for url in product_category.keys():
            meta = {
                "category_name": product_category.get(url)
            }
            yield scrapy.Request(url, meta=meta, callback=self.parse_product_list)
