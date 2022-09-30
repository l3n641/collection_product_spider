from ..libs.product_excel import ProductExcel
from ..models import Base, ProductUrl, FailedCategory
from ..libs.sqlite import Sqlite
from scrapy.utils.project import get_project_settings
import os
import scrapy
from ..items import ProductUrlItem, ProductDetailItem


class CommonIndirectSpider(scrapy.Spider):
    project_name = None
    check_lang = True

    def __init__(self, action, category_file=None, *args, **kwargs):

        super(CommonIndirectSpider).__init__(*args, **kwargs)
        self.action = int(action)

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

        db_engine = Sqlite.get_sqlite_engine(file.project_name, project_settings.get("DB_DIR_PATH"))
        Sqlite.set_session_class(db_engine)
        Base.metadata.create_all(db_engine)

    def start_requests(self):
        if self.action == 1:
            urls = self.get_start_urls()
            args = self.get_request_product_list_args()
            for item in urls:
                yield scrapy.Request(item.get("url"), meta=item.get("meta"), callback=self.parse_product_list, **args)

        else:

            data = self.get_failed_detail_urls()
            for item in data:
                request_data = self.get_product_detail_request_args(item)
                yield scrapy.Request(**request_data)

    def get_request_product_list_args(self):
        return {
            "errback": self.start_request_error,
            "dont_filter": True
        }

    def get_start_urls(self):
        return self.get_start_url_by_category()

    def get_start_url_by_category(self):
        product_category = self.product_category
        data_list = []
        for url in product_category.keys():
            meta = {
                "category_name": product_category.get(url),
                "referer": url,
            }
            item = {
                "url": url,
                "meta": meta
            }
            data_list.append(item)
        return data_list

    @staticmethod
    def start_request_error(failure):
        session = Sqlite.get_session()
        data = {
            'url': failure.request.meta.get("referer"),
            'category_name': failure.request.meta.get("category_name"),
        }
        log = FailedCategory(**data)
        session.add(log)
        session.commit()
        print(f"excel 链接无效:{failure.request.url}")

    @staticmethod
    def get_product_log(detail_url, category_name):
        session = Sqlite.get_session()
        data = session.query(ProductUrl).filter(ProductUrl.url == detail_url,
                                                ProductUrl.category_name == category_name).first()
        return data

    def add_product_detail_url(self, detail_url, category_name, referer, page_url, ):
        """
        请求详情页面
        :param detail_url:
        :param category_name:
        :param referer:
        :param page_url:
        :return:
        """

        data = self.get_product_log(detail_url, category_name)
        if not data:
            item_data = {
                "category_name": category_name,
                "url": detail_url,
                "referer": referer,
                "status": 0,
                "page_url": page_url,
            }
            yield ProductUrlItem(**item_data)

    @staticmethod
    def get_failed_detail_urls():
        """
        获取失败的详情链接
        :return: [ProductUrl]
        """
        session = Sqlite.get_session()
        data = session.query(ProductUrl).filter(ProductUrl.status == 0).all()
        return data

    def get_product_detail_request_args(self, item: ProductUrl):
        """
        获取重新详情页面的请求参数
        :param item:
        :return:
        """
        meta = {
            "category_name": item.category_name,
            "referer": item.referer,

        }
        item_data = {
            "url": item.url,
            "meta": meta,
            "callback": self.parse_product_detail,
        }
        return item_data
