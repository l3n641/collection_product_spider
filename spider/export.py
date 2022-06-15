import os.path

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from html_website_spider.models import ProductUrl, ProductDetail
from html_website_spider.libs.product_excel import ProductExcel
import click


def get_sqlite_session(database_file_name):
    engine = create_engine(f"sqlite:///{database_file_name}", echo=False, poolclass=StaticPool,
                           connect_args={'check_same_thread': False})
    Session = sessionmaker(bind=engine)
    return Session()


def filter_empty_image(product_detail_data, image_path):
    new_product_detail_data = []
    for item in product_detail_data:
        image_dir = os.path.join(image_path, item.sku)
        if not os.path.exists(image_dir):
            msg = f"sku:{item.sku},图片不存在"
            print(msg)
            continue
        new_product_detail_data.append(item)
    return new_product_detail_data


def export_to_excel(database_file_name, excel_path, filter_by="sku", image_path=None, default_brand=None):
    if not os.path.exists(database_file_name):
        raise ValueError("file not found")
    session = get_sqlite_session(database_file_name)
    data = session.query(ProductUrl).all()
    file = ProductExcel(excel_path)
    product_list = []
    for item in data:
        product_list.append({"url": item.url, "category": item.category_name})
    file.write_product_list(product_list)

    query = session.query(ProductDetail)
    if filter_by:
        query = query.group_by(getattr(ProductDetail, filter_by))

    product_detail_data = query.all()

    if image_path:
        product_detail_data = filter_empty_image(product_detail_data, image_path)

    file.write_product_detail(product_detail_data, default_brand)


if __name__ == "__main__":
    excel_path = "F:\collection\\10012_zara_fr.xlsx"
    default_brand = "H&M"
    image_path = "F:\scrapy_down\\10012_zara_fr"
    database_file_name = "F:\code\collection_product_spider\spider\data\\10012_zara_fr"
    export_to_excel(database_file_name, excel_path, image_path=image_path, default_brand=default_brand)
