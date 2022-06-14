import os.path

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from spider.models import ProductUrl, ProductDetail
from spider.libs.productExcel import ProductExcel
import click


def get_sqlite_session(database_file_name):
    engine = create_engine(f"sqlite:///{database_file_name}", echo=False, poolclass=StaticPool,
                           connect_args={'check_same_thread': False})
    Session = sessionmaker(bind=engine)
    return Session()


@click.command()
@click.option('--database_file_name', help='sqlite数据库文件路径')
@click.option('--excel_path', help='excel 文件路径')
@click.option('--project_name', help='项目名称')
def export_to_excel(database_file_name, excel_path, project_name):
    if not os.path.exists(database_file_name):
        raise ValueError("file not found")
    session = get_sqlite_session(database_file_name)
    data = session.query(ProductUrl).all()
    file = ProductExcel(excel_path)
    product_list = []
    for item in data:
        product_list.append({"url": item.url, "category": item.category_name})
    file.write_product_list(product_list)

    product_detail_data = session.query(ProductDetail).all()
    file.write_product_detail(product_detail_data, project_name, "H&M")


if __name__ == "__main__":
    export_to_excel()
