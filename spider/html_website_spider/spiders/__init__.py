# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from ..items import ProductUrlItem, ProductDetailItem
from ..libs.product_excel import ProductExcel
from ..models import Base, ProductUrl, FailedCategory
from ..libs.sqlite import Sqlite
from ..libs.browser.chrome_browser import ChromeBrowser
