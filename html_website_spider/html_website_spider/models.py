from sqlalchemy import Column, String, create_engine, Integer, Text, DATETIME
from sqlalchemy.ext.declarative import declarative_base

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
    price = Column(Text)
    title = Column(Text)
    dade = Column(DATETIME)
    basc = Column(Text)
    brand = Column(Text)
    img = Column(Text)
