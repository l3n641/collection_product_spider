import os.path

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker


def get_sqlite_session(database_file_name):
    engine = create_engine(f"sqlite:///{database_file_name}", echo=False, poolclass=StaticPool,
                           connect_args={'check_same_thread': False})
    session_class = sessionmaker(bind=engine)
    return session_class()


def filter_empty_image(product_detail_data, image_path):
    new_product_detail_data = []
    failed_image_sku = []
    failed_first_image_sku = []
    error_sku_img = []
    for item in product_detail_data:
        image_dir = os.path.join(image_path, item.sku)
        if not os.path.exists(image_dir):
            failed_image_sku.append(item.sku)
            continue
        if not os.path.exists(os.path.join(image_dir, '1.jpg')):
            failed_first_image_sku.append(item.sku)
            failed_image_sku.append(item.sku)
            continue
        images = item.img.split("|")
        for image in images:
            if item.sku not in image:
                error_sku_img.append(item.sku)
                failed_image_sku.append(item.sku)
                break

        new_product_detail_data.append(item)
        failed_image_info = {
            "failed_image_sku": failed_image_sku,
            "failed_first_image_sku": failed_first_image_sku,
            "error_sku_img": error_sku_img,
        }
    return new_product_detail_data, failed_image_info


def merge_product_category(product_detail_data: list, field: str):
    """
    根据指定字段合并产品分类
    :param product_detail_data:
    :param field:
    :return:
    """
    new_product_detail_data = []
    product_dict = {}
    for product in product_detail_data:
        key = getattr(product, field)
        if key not in product_dict.keys():
            product_dict[key] = []

        product_dict[key].append(product)

    for key in product_dict:
        category_name_set = set()
        for data in product_dict[key]:
            category_name_set.add(data.category_name)

        data.category_name = '|'.join(category_name_set)
        new_product_detail_data.append(data)

    return new_product_detail_data
