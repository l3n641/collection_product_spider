# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from data_export_tools.views.ui_main_window import Ui_MainWindow
from dotenv import load_dotenv
from PySide6.QtCore import QDir
from functions import get_sqlite_session
from spider.html_website_spider.libs.product_excel import ProductExcel
from PySide6.QtGui import QTextCursor
from spider.html_website_spider.models import ProductDetail
from functions import filter_empty_image


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
        self.main_view.button_load_project.clicked.connect(self.load_project_file)
        self.main_view.button_check_data.clicked.connect(self.check_data)
        self.main_view.button_set_default_brand.clicked.connect(self.set_default_brand)
        self.main_view.button_export_data.clicked.connect(self.export_data)

    def load_project_file(self):
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

        self.database_file = database_file
        self.image_dir = image_dir
        self.main_view.label_project_file.setText(file_path)

        session = get_sqlite_session(database_file)
        product_details = session.query(ProductDetail).all()
        self.product_details = product_details
        self.main_view.input_total_quantity.setText(str(len(product_details)))

        self.main_view.textarea_log.moveCursor(QTextCursor.End)
        self.main_view.textarea_log.append("加载成功")

    def check_data(self):
        session = get_sqlite_session(self.database_file)
        query = session.query(ProductDetail)
        field = self.main_view.input_repeat_quantity.text()
        filer_price = self.main_view.input_filter_min_price.text()
        is_filter_image = self.main_view.check_box_filter_image.isChecked()
        if field:
            query = query.group_by(getattr(ProductDetail, field))
        if filer_price:
            query = query.filter(ProductDetail.price >= filer_price)
        product_detail_datas = query.all()

        if is_filter_image:
            product_detail_datas, failed_image_sku_list = filter_empty_image(product_detail_datas, self.image_dir)
            for item in failed_image_sku_list:
                self.main_view.textarea_log.moveCursor(QTextCursor.End)
                self.main_view.textarea_log.append(f"产品{item},下载图片失败")

            self.main_view.input_image_failed_quantity.setText(str(len(failed_image_sku_list)))

        self.main_view.input_validate_quantity.setText(str(len(product_detail_datas)))
        self.product_details = product_detail_datas

    def set_default_brand(self):
        self.default_brand = self.main_view.input_default_brand.text()
        QMessageBox.information(self, "信息", "设置默认品牌成功", QMessageBox.Yes)

    def export_data(self):
        self.product_file.write_product_detail(self.product_details, self.default_brand)
        QMessageBox.information(self, "信息", "导出完成", QMessageBox.Yes)


if __name__ == "__main__":
    load_dotenv()

    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
