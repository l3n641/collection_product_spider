from sqlalchemy import Column, String, create_engine, Integer, Text, DATETIME, Float
from sqlalchemy.ext.declarative import declarative_base
import re

# 创建对象的基类:
Base = declarative_base()


class ProductUrl(Base):
    __tablename__ = 'product_urls'

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    url = Column(String(1024), nullable=False)
    category_name = Column(String(128), nullable=False)
    referer = Column(String(1024), nullable=False, comment="从哪个地址下载")


class ProductDetail(Base):
    __tablename__ = 'product_detail'

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    PageUrl = Column(Text, nullable=False)
    category_name = Column(String(128))
    sku = Column(String(32))
    color = Column(Text)
    size = Column(Text)
    price = Column(Float)
    title = Column(Text)
    dade = Column(DATETIME)
    basc = Column(Text)
    brand = Column(Text)
    img = Column(Text)

    @property
    def featured_image(self):
        if not self.img:
            return
        pattern = 'src="(.*?)"'
        result = re.search(pattern, self.img)
        if not result:
            return

        return result.group(1)

    @property
    def gender(self):
        if self.category_name:
            category_names = self.category_name.split("|")
            gender = category_names[0].split('->')[0]
            return gender

    @property
    def cat_0(self):
        cat_0_set = set()
        if self.category_name:
            category_names = self.category_name.split("|")
            for category in category_names:
                cat_0 = category.split('->')[1]
                cat_0_set.add(cat_0)

            return "|".join(cat_0_set)

    @property
    def category_type(self):
        category_type_set = set()
        if self.category_name:
            category_names = self.category_name.split("|")
            for category in category_names:
                category_type = category.split('->')[2]
                category_type_set.add(category_type)
            return "|".join(category_type_set)

    def get_brand(self, default_brand=None):
        return self.brand or default_brand


class DownloadImageLog(Base):
    __tablename__ = 'download_image_log'

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    sku = Column(String(32))
    url = Column(Text, nullable=False)
    status = Column(Integer, nullable=False)
    local_path = Column(Text)
