from ..models import ProductUrl, FailedCategory
from ..libs.sqlite import Sqlite
import scrapy
from ..items import ProductUrlItem, ProductDetailItem
from .common_spider import CommonSpider


class CommonIndirectSpider(CommonSpider):

    def start_requests(self):
        if self.action == 1:
            for task in self.start_by_product_category():
                yield task

        else:
            data = self.get_failed_detail_urls()
            for item in data:
                request_data = self.get_product_detail_request_args(item)
                yield scrapy.Request(**request_data)

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
