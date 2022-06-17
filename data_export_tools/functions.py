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
    for item in product_detail_data:
        image_dir = os.path.join(image_path, item.sku)
        if not os.path.exists(image_dir):
            failed_image_sku.append(item.sku)
            continue
        new_product_detail_data.append(item)
    return new_product_detail_data, failed_image_sku
