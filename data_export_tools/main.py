# This Python file uses the following encoding: utf-8
import datetime
import os
from pathlib import Path
import sys
from sqlalchemy import func, distinct
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from data_export_tools.views.ui_main_window import Ui_MainWindow
from dotenv import load_dotenv
from PySide6.QtCore import QDir
from functions import get_sqlite_session, merge_product_category
from spider.html_website_spider.libs.product_excel import ProductExcel
from PySide6.QtGui import QTextCursor
from spider.html_website_spider.models import ProductDetail, ProductUrl
from functions import filter_empty_image
from size_guide import SizeGuide
from server import DatabaseSqlite
from pre_product import PreProductExcel


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_view = Ui_MainWindow()
        self.main_view.setupUi(self)
        self.database_file = None
        self.image_dir = None
        self.default_brand = None
        self.product_file = None
        self.product_details = []
        self.category_data = None
        self.main_view.button_load_project.clicked.connect(self.load_project_file)
        self.main_view.button_check_data.clicked.connect(self.check_data)
        self.main_view.button_set_default_brand.clicked.connect(self.set_default_brand)
        self.main_view.button_export_data.clicked.connect(self.export_data)
        self.main_view.button_clear_log.clicked.connect(self.clear_log)


    def load_project_file(self):
        """
        加载项目数据
        :return:
        """
        project_path = os.getenv("PROJECT_STORE", QDir.currentPath())
        file_path, _ = QFileDialog.getOpenFileName(self, "请选择文件", project_path, "产品类目(*.xlsx)")
        if not file_path:
            return
        file = ProductExcel(file_path)
        self.product_file = file
        database_file = os.path.join(project_path, "database", file.project_name + ".db")
        image_dir = os.path.join(project_path, "image", file.project_name)

        if not os.path.exists(database_file):
            QMessageBox.critical(self, "错误", "数据库文件不存在", QMessageBox.Yes, QMessageBox.Yes)
            return False

        if not os.path.exists(image_dir):
            QMessageBox.critical(self, "错误", "图片目录不存在", QMessageBox.Yes, QMessageBox.Yes)
            return False

        category_data = file.get_category()
        if not category_data:
            QMessageBox.critical(self, "错误", "加载文件失败", QMessageBox.Yes, QMessageBox.Yes)
            return False

        self.category_data = category_data
        self.database_file = database_file
        self.image_dir = image_dir
        self.main_view.label_project_file.setText(file_path)

        db_server = DatabaseSqlite(database_file)
        product_details = db_server.get_product_detail_all()

        self.product_details = product_details
        self.main_view.input_total_quantity.setText(str(len(product_details)))
        spider_base_url_quantity = db_server.get_spider_category_amount()
        categories = file.get_category()

        self.main_view.textarea_log.clear()
        self.main_view.textarea_log.append("加载成功")
        self.main_view.textarea_log.append(f"excel 包含链接数:{len(categories)}")
        self.main_view.textarea_log.append(f"实际爬取基础链接数:{spider_base_url_quantity}")

        not_spider_categories = db_server.get_not_spider_category(categories)
        for record in not_spider_categories:
            self.main_view.textarea_log.append(f"没有爬取的分类:{record.get('category')} : {record.get('url')}")

    def merge_product_category(self):
        db_server = DatabaseSqlite(self.database_file)
        for product in self.product_details:
            categories = db_server.get_product_categories(product.PageUrl, self.category_data)
            product.category_name = categories
        self.main_view.textarea_log.append("合并产品分类成功")

    def clear_log(self):
        self.main_view.textarea_log.clear()

    def check_data(self):
        self.main_view.textarea_log.moveCursor(QTextCursor.End)
        self.main_view.textarea_log.append("开始检测产品，请等待")
        filter_filed = None
        if self.main_view.checkbox_filter_repeat_sku_product.isChecked():
            filter_filed = 'sku'
        filer_price = self.main_view.input_filter_min_price.text()
        is_filter_image = self.main_view.check_box_filter_image.isChecked()

        db_server = DatabaseSqlite(self.database_file)
        product_detail_datas = db_server.get_product_detail_all(filter_filed, filer_price)

        if is_filter_image:
            product_detail_datas, failed_image_info = filter_empty_image(product_detail_datas, self.image_dir)

            for item in failed_image_info.get("failed_image_sku"):
                self.main_view.textarea_log.append(f"{item},下载图片失败")

            for item in failed_image_info.get("failed_first_image_sku"):
                self.main_view.textarea_log.append(f"{item},首图下载失败")

            for item in failed_image_info.get("error_sku_img"):
                self.main_view.textarea_log.append(f"{item},图片和sku不一致")
            failed_total = len(failed_image_info.get("failed_image_sku")) + len(
                failed_image_info.get("failed_first_image_sku")) + len(failed_image_info.get("error_sku_img"))
            self.main_view.input_image_failed_quantity.setText(str(failed_total))
            self.main_view.textarea_log.moveCursor(QTextCursor.End)
            self.main_view.textarea_log.append(f"检测完成，可以导出产品：{datetime.datetime.now()}")

        self.main_view.input_validate_quantity.setText(str(len(product_detail_datas)))
        self.product_details = product_detail_datas

    def set_default_brand(self):
        self.default_brand = self.main_view.input_default_brand.text()
        QMessageBox.information(self, "信息", "设置默认品牌成功", QMessageBox.Yes)

    def export_data(self):
        self.merge_product_category()
        save_dir = os.path.dirname(self.product_file.path)
        export_dir = os.path.join(save_dir, "export")
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        export_path = os.path.join(export_dir, self.product_file.file_name)
        state = self.product_file.write_product_detail(self.product_details, self.default_brand,
                                                       export_path=export_path)

        if state:
            QMessageBox.information(self, "信息", "导出完成", QMessageBox.Yes)
        else:
            QMessageBox.critical(self, "错误", "导出数据失败", QMessageBox.Yes, QMessageBox.Yes)


if __name__ == "__main__":
    load_dotenv()

    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
