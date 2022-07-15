from ..libs.product_excel import ProductExcel
from ..models import Base, ProductUrl
from ..libs.sqlite import Sqlite
from scrapy.utils.project import get_project_settings
import os
import scrapy
from ..items import ProductUrlItem, ProductDetailItem


class CommonSpider(scrapy.Spider):
    project_name = None
    check_lang = True

    def __init__(self, category_file=None, is_continue=True, *args, **kwargs):

        super(CommonSpider).__init__(*args, **kwargs)

        project_settings = get_project_settings()
        category_file_path = os.path.join(project_settings.get("PROJECT_STORE"), category_file)

        if not os.path.exists(category_file_path):
            raise ValueError("产品类别文件不存在")

        file = ProductExcel(category_file_path)
        if self.check_lang:
            spider_data = self.name.split("_")

            lang = spider_data[-1] if len(spider_data) > 1 else "en"
            if file.lange.upper() != lang.upper():
                raise ValueError("任务文件和爬虫语言不匹配")

        product_category = file.get_category()
        self.product_category = product_category
        self.project_name = file.project_name
        self.is_continue = is_continue

        if not is_continue:
            # 重头开始下载内容
            Sqlite.rename_old_database(file.project_name, project_settings.get("DB_DIR_PATH"))

        db_engine = Sqlite.get_sqlite_engine(file.project_name, project_settings.get("DB_DIR_PATH"))
        Sqlite.set_session_class(db_engine)
        Base.metadata.create_all(db_engine)

    def start_requests(self):
        product_category = self.product_category
        for url in product_category.keys():
            meta = {
                "category_name": product_category.get(url),
                "referer": url,

            }
            yield scrapy.Request(url, meta=meta, callback=self.parse_product_list, errback=self.start_request_error,
                                 dont_filter=True)

    @staticmethod
    def start_request_error(failure):
        print(f"excel 链接无效:{failure.request.url}")

    def request_product_detail(self, detail_url, category_name, referer, **kwargs):
        """
        请求详情页面
        :param detail_url:
        :param category_name:
        :param referer:
        :param kwargs:
        :return:
        """
        # 如果开启断点续传就从数据库获取数据后判断
        if self.is_continue:
            session = Sqlite.get_session()
            data = session.query(ProductUrl).filter(ProductUrl.url == detail_url,
                                                    ProductUrl.category_name == category_name,
                                                    ProductUrl.status == 1).first()
            if data:
                return False

        item_data = {
            "category_name": category_name,
            "url": detail_url,
            "referer": referer,
        }
        yield ProductUrlItem(**item_data)
        yield scrapy.Request(detail_url, **kwargs)
