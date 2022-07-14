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
        self.main_view.combobox_size_temolate.currentTextChanged.connect(self.get_size_tmp_detail)
        self.main_view.button_update_size.clicked.connect(self.update_size_by_category)
        self.main_view.combo_box_category.currentTextChanged.connect(self.set_category_to_category_size_input)
        self.main_view.combobox_category_name.currentTextChanged.connect(self.set_category_to_old_category_input)
        self.main_view.button_upate_category_name.clicked.connect(self.update_category_name)

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

        category_data = file.get_category()
        if not category_data:
            QMessageBox.critical(self, "错误", "加载文件失败", QMessageBox.Yes, QMessageBox.Yes)
            return False

        for url in category_data:
            self.main_view.combo_box_category.addItem(category_data.get(url))
            self.main_view.combobox_category_name.addItem(category_data.get(url))

        data = SizeGuide.get_size_name_list()
        self.main_view.combobox_size_temolate.addItems(data)

        self.database_file = database_file
        self.image_dir = image_dir
        self.main_view.label_project_file.setText(file_path)

        session = get_sqlite_session(database_file)
        product_details = session.query(ProductDetail).all()
        self.product_details = product_details
        self.main_view.input_total_quantity.setText(str(len(product_details)))

        self.main_view.textarea_log.moveCursor(QTextCursor.End)
        self.main_view.textarea_log.append("加载成功")
        categories = file.get_category()
        self.main_view.textarea_log.append(f"excel 包含链接数:{len(categories)}")

        spider_base_url_quantity, *_ = session.query(func.count(distinct(ProductUrl.referer))).first()
        self.main_view.textarea_log.append(f"实际爬取基础链接数:{spider_base_url_quantity}")
        not_spider_categories = self.get_not_spider_category(categories, session)
        for record in not_spider_categories:
            self.main_view.textarea_log.append(f"没有爬取的分类:{record.get('category')} : {record.get('url')}")

    @staticmethod
    def get_not_spider_category(categories, session):
        """
        获取没有爬取到的产品分类
        :param categories:
        :param session:
        :return:
        """
        spider_category_urls = session.query(distinct(ProductUrl.referer)).all()

        not_spider_urls = []
        for url in categories.keys():
            state = False
            for spider_url, *_ in spider_category_urls:
                if url.startswith(spider_url):
                    state = True
                    break
            if not state:
                not_spider_urls.append({"category": categories.get(url), "url": url})

        return not_spider_urls

    def check_data(self):
        self.main_view.textarea_log.moveCursor(QTextCursor.End)
        self.main_view.textarea_log.append("开始检测产品，请等待")

        session = get_sqlite_session(self.database_file)
        query = session.query(ProductDetail)
        methods = self.main_view.select_data_process_method.currentIndex()
        filter_filed = self.main_view.input_filter_field.text()
        filer_price = self.main_view.input_filter_min_price.text()
        is_filter_image = self.main_view.check_box_filter_image.isChecked()

        if methods == 1 and filter_filed:
            # 如果是过滤重复产品
            query = query.group_by(getattr(ProductDetail, filter_filed))
            if filer_price:
                query = query.having(ProductDetail.price >= filer_price)

        else:
            if filer_price:
                query = query.filter(ProductDetail.price >= filer_price)

        product_detail_datas = query.all()

        if is_filter_image:
            product_detail_datas, failed_image_info = filter_empty_image(product_detail_datas, self.image_dir)

            for item in failed_image_info.get("failed_image_sku"):
                self.main_view.textarea_log.moveCursor(QTextCursor.End)
                self.main_view.textarea_log.append(f"{item},下载图片失败")

            for item in failed_image_info.get("failed_first_image_sku"):
                self.main_view.textarea_log.moveCursor(QTextCursor.End)
                self.main_view.textarea_log.append(f"{item},首图下载失败")

            for item in failed_image_info.get("error_sku_img"):
                self.main_view.textarea_log.moveCursor(QTextCursor.End)
                self.main_view.textarea_log.append(f"{item},图片和sku不一致")
            failed_total = len(failed_image_info.get("failed_image_sku")) + len(
                failed_image_info.get("failed_first_image_sku")) + len(failed_image_info.get("error_sku_img"))
            self.main_view.input_image_failed_quantity.setText(str(failed_total))
            self.main_view.textarea_log.moveCursor(QTextCursor.End)
            self.main_view.textarea_log.append(f"检测完成，可以导出产品：{datetime.datetime.now()}")
        if methods == 2:
            # 如果是合并产品
            product_detail_datas = merge_product_category(product_detail_datas, filter_filed)

        self.main_view.input_validate_quantity.setText(str(len(product_detail_datas)))
        self.product_details = product_detail_datas

    def set_default_brand(self):
        self.default_brand = self.main_view.input_default_brand.text()
        QMessageBox.information(self, "信息", "设置默认品牌成功", QMessageBox.Yes)

    def export_data(self):
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

    def get_size_tmp_detail(self, value):
        data = value.split("->")
        res = SizeGuide.get_default_size(*data)
        if res:
            self.main_view.input_size.setText('|'.join(res))

    def set_category_to_category_size_input(self, value):
        self.main_view.input_category_pattern.setText(value)

    def set_category_to_old_category_input(self, value):
        self.main_view.input_category_name_pattern.setText(value)

    def update_category_name(self):
        new_category_name = self.main_view.input_new_category_name.text()
        category = self.main_view.input_category_name_pattern.text()
        row = 0
        for item in self.product_details:
            if item.category_name and item.category_name.startswith(category):
                item.category_name = new_category_name
                row = row + 1

        self.main_view.textarea_log.append(f"类别:{category},更新类别名称{new_category_name}，更新数量{row}")

    def update_size_by_category(self):
        new_size = self.main_view.input_size.text()
        category = self.main_view.input_category_pattern.text()
        row = 0
        for item in self.product_details:
            if item.category_name and item.category_name.startswith(category):
                item.size = new_size
                row = row + 1

        self.main_view.textarea_log.append(f"类别:{category},更新尺码{new_size}，更新数量{row}")


if __name__ == "__main__":
    load_dotenv()

    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
