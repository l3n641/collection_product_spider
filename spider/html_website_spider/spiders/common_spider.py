from ..libs.product_excel import ProductExcel
from ..models import Base, ProductUrl, FailedCategory
from ..libs.sqlite import Sqlite
from scrapy.utils.project import get_project_settings
import os
import scrapy
from ..items import ProductUrlItem, ProductDetailItem


class CommonSpider(scrapy.Spider):
    project_name = None
    check_lang = True

    def __init__(self, category_file=None, is_continue=True, start_by_failed=False, *args, **kwargs):

        super(CommonSpider).__init__(*args, **kwargs)
        is_continue = int(is_continue)

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
        if not product_category:
            raise ValueError("打开excel 文件失败")
        self.product_category = product_category
        self.project_name = file.project_name
        self.is_continue = is_continue
        self.start_by_failed = start_by_failed

        if not is_continue:
            # 重头开始下载内容
            Sqlite.rename_old_database(file.project_name, project_settings.get("DB_DIR_PATH"))

        db_engine = Sqlite.get_sqlite_engine(file.project_name, project_settings.get("DB_DIR_PATH"))
        Sqlite.set_session_class(db_engine)
        Base.metadata.create_all(db_engine)

    def start_requests(self):
        if self.start_by_failed:
            for task in self.start_by_database():
                yield task
        else:
            for task in self.start_by_product_category():
                yield task

    def start_by_product_category(self):
        """
        从产品分类里爬取数据
        :return:
        """
        product_category = self.product_category
        for url in product_category.keys():
            meta = {
                "category_name": product_category.get(url),
                "referer": url,

            }
            yield scrapy.Request(url, meta=meta, callback=self.parse_product_list, errback=self.start_request_error,
                                 dont_filter=True)

    def start_by_database(self):
        """
        从数据失败记录里开始
        :return:
        """
        data = self.get_failed_detail_urls()
        for item in data:
            request_data = self.get_failed_quest_data(item)
            yield scrapy.Request(**request_data)

    def get_failed_quest_data(self, item: ProductUrl, **kwargs):
        """
        获取重新下载失败的详情页面的参数
        :param item:
        :param kwargs:
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
        item_data.update(kwargs)
        return item_data

    @staticmethod
    def get_failed_detail_urls():
        """
        获取失败的详情链接
        :return: [ProductUrl]
        """
        session = Sqlite.get_session()
        data = session.query(ProductUrl).filter(ProductUrl.status == 0).all()
        return data

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

    def request_product_detail(self, detail_url, category_name, referer, page_url, **kwargs):
        """
        请求详情页面
        :param detail_url:
        :param category_name:
        :param referer:
        :param page_url:
        :param kwargs:
        :return:
        """
        # 如果开启断点续传就从数据库获取数据后判断
        data = None  # 数据库记录
        if self.is_continue:
            data = self.get_product_log(detail_url, category_name)
            if data and data.status == 1:
                return False

        if not data:
            item_data = {
                "category_name": category_name,
                "url": detail_url,
                "referer": referer,
                "status": 0,
                "page_url": page_url,
            }
            yield ProductUrlItem(**item_data)
        yield scrapy.Request(detail_url, **kwargs)
