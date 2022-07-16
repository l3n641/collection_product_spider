# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from ..items import ProductUrlItem, ProductDetailItem
from ..libs.product_excel import ProductExcel
from ..models import Base, ProductUrl
from ..libs.sqlite import Sqlite