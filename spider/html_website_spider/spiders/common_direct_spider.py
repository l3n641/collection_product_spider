from .common_spider import CommonSpider


class CommonDirectSpider(CommonSpider):

    def start_requests(self):
        for task in self.start_by_product_category():
            yield task
