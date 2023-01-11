from ..libs.product_excel import ProductExcel
from ..models import Base, ProductUrl, FailedCategory
from ..libs.sqlite import Sqlite
from scrapy.utils.project import get_project_settings
import os
import scrapy
from ..items import ProductUrlItem
import hashlib
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qsl


class CommonSpider(scrapy.Spider):
    """ 爬虫基类"""
    project_name = None

    def __init__(self, category_file=None, is_continue=True, start_by_failed=False, check_lang=True, *args, **kwargs):

        super(CommonSpider).__init__(*args, **kwargs)
        is_continue = int(is_continue)
        check_lang = int(check_lang)

        project_settings = get_project_settings()
        category_file_path = os.path.join(project_settings.get("PROJECT_STORE"), category_file)

        if not os.path.exists(category_file_path):
            raise ValueError("产品类别文件不存在")

        file = ProductExcel(category_file_path)
        if check_lang:
            spider_data = self.name.split("_")

            lang = spider_data[-1] if len(spider_data) > 1 else "en"
            if file.lange.upper() != lang.upper():
                raise ValueError("任务文件和爬虫语言不匹配")

        product_category = file.get_category()
        if not product_category:
            raise ValueError("打开excel 文件失败")
        self.product_category = product_category
        self.project_name = file.project_name
        self.start_by_failed = start_by_failed

        if not is_continue:
            # 重头开始下载内容
            Sqlite.rename_old_database(file.project_name, project_settings.get("DB_DIR_PATH"))

        db_engine = Sqlite.get_sqlite_engine(file.project_name, project_settings.get("DB_DIR_PATH"))
        Sqlite.set_session_class(db_engine)
        Base.metadata.create_all(db_engine)

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
    def get_product_log(detail_url, category_name=None):
        session = Sqlite.get_session()
        data = session.query(ProductUrl).filter(ProductUrl.url == detail_url)
        if category_name:
            data = data.filter(ProductUrl.category_name == category_name)
        return data.first()

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

        data = self.get_product_log(detail_url, category_name)
        if data and data.status == 1:
            return False
        else:
            item_data = {
                "category_name": category_name,
                "url": detail_url,
                "referer": referer,
                "status": 0,
                "page_url": page_url,
            }
            yield ProductUrlItem(**item_data)
            yield scrapy.Request(detail_url, **kwargs)

    def get_request_product_list_args(self):
        return {
            "errback": self.start_request_error,
            "dont_filter": True
        }

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

    @staticmethod
    def get_url_md5(url):
        """获取链接md5"""
        url_hash = hashlib.md5(url.encode(encoding='UTF-8')).hexdigest()
        return url_hash

    @staticmethod
    def get_url_params(url):
        """获取url链接参数"""
        url_info = urlparse(url)
        params = dict(parse_qsl(url_info.query))
        return params

    @staticmethod
    def make_url_with_query(base_url, params: dict):
        query = urlencode(params)
        return base_url + "?" + query

    @staticmethod
    def get_base_url(url):
        info = urlparse(url)
        return f"{info.scheme}://{info.hostname}{info.path}"
