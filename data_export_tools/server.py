from functions import get_sqlite_session
from spider.html_website_spider.models import ProductDetail, ProductUrl
from sqlalchemy import func, distinct


class DatabaseSqlite(object):
    def __init__(self, db_file_path):
        self.db_file_path = db_file_path
        self.session = get_sqlite_session(db_file_path)

    def get_spider_category_amount(self):
        spider_base_url_quantity, *_ = self.session.query(func.count(distinct(ProductUrl.referer))).first()
        return spider_base_url_quantity

    def get_not_spider_category(self, categories):
        """
        获取没有爬取到的产品分类
        :param categories:
        :param session:
        :return:
        """
        spider_category_urls = self.session.query(distinct(ProductUrl.referer)).all()

        not_spider_urls = []
        for url in categories.keys():
            state = False
            for spider_url, *_ in spider_category_urls:
                if url.startswith(spider_url):
                    state = True
                    break
            if not state:
                not_spider_urls.append({"category": categories.get(url), "url": url})

        return not_spider_urls

    def get_product_detail_all(self, filter_filed=None, filer_price=None):
        query = self.session.query(ProductDetail)
        if filter_filed:
            # 如果是过滤重复产品
            query = query.group_by(getattr(ProductDetail, filter_filed))
        if filer_price:
            # 如果是过滤产品价格
            query = query.filter(ProductDetail.price >= filer_price)

        product_detail_datas = query.all()
        return product_detail_datas

    def get_product_categories(self, product_url):
        query = self.session.query(ProductUrl)
        data = query.filter(ProductUrl.url == product_url).all()
        categories = (item.category_name for item in data)
        return '|'.join(categories)

    def update_product_category(self, product_detail_data):
        for product in product_detail_data:
            categories = self.get_product_categories(product.PageUrl)
            if categories:
                product.category_name = categories
        return product_detail_data
