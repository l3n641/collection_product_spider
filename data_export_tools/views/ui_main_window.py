# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget,
    QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1105, 736)
        MainWindow.setStyleSheet(u"backgroud-color:rgb(205, 205, 205)")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_6 = QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_9 = QGridLayout(self.tab)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.input_filter_min_price = QLineEdit(self.groupBox)
        self.input_filter_min_price.setObjectName(u"input_filter_min_price")

        self.gridLayout_2.addWidget(self.input_filter_min_price, 0, 4, 1, 1)

        self.checkbox_filter_repeat_sku_product = QCheckBox(self.groupBox)
        self.checkbox_filter_repeat_sku_product.setObjectName(u"checkbox_filter_repeat_sku_product")
        self.checkbox_filter_repeat_sku_product.setChecked(True)

        self.gridLayout_2.addWidget(self.checkbox_filter_repeat_sku_product, 0, 2, 1, 1)

        self.checkbox_filter_invalidate_product = QCheckBox(self.groupBox)
        self.checkbox_filter_invalidate_product.setObjectName(u"checkbox_filter_invalidate_product")
        self.checkbox_filter_invalidate_product.setChecked(True)

        self.gridLayout_2.addWidget(self.checkbox_filter_invalidate_product, 0, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 0, 3, 1, 1)

        self.button_check_data = QPushButton(self.groupBox)
        self.button_check_data.setObjectName(u"button_check_data")

        self.gridLayout_2.addWidget(self.button_check_data, 0, 6, 1, 1)

        self.check_box_filter_image = QCheckBox(self.groupBox)
        self.check_box_filter_image.setObjectName(u"check_box_filter_image")
        self.check_box_filter_image.setChecked(True)

        self.gridLayout_2.addWidget(self.check_box_filter_image, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.groupBox, 1, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.tab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout = QGridLayout(self.groupBox_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.button_load_project = QPushButton(self.groupBox_4)
        self.button_load_project.setObjectName(u"button_load_project")

        self.gridLayout.addWidget(self.button_load_project, 0, 0, 1, 1)

        self.button_set_default_brand = QPushButton(self.groupBox_4)
        self.button_set_default_brand.setObjectName(u"button_set_default_brand")

        self.gridLayout.addWidget(self.button_set_default_brand, 0, 2, 1, 1)

        self.input_default_brand = QLineEdit(self.groupBox_4)
        self.input_default_brand.setObjectName(u"input_default_brand")

        self.gridLayout.addWidget(self.input_default_brand, 0, 3, 1, 1)

        self.label_project_file = QLabel(self.groupBox_4)
        self.label_project_file.setObjectName(u"label_project_file")

        self.gridLayout.addWidget(self.label_project_file, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.groupBox_4, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_5 = QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_5.addWidget(self.label_4, 0, 6, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)

        self.input_validate_quantity = QLineEdit(self.groupBox_2)
        self.input_validate_quantity.setObjectName(u"input_validate_quantity")
        self.input_validate_quantity.setReadOnly(True)

        self.gridLayout_5.addWidget(self.input_validate_quantity, 0, 3, 1, 1)

        self.button_export_data = QPushButton(self.groupBox_2)
        self.button_export_data.setObjectName(u"button_export_data")

        self.gridLayout_5.addWidget(self.button_export_data, 0, 8, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_5.addWidget(self.label_2, 0, 2, 1, 1)

        self.input_image_failed_quantity = QLineEdit(self.groupBox_2)
        self.input_image_failed_quantity.setObjectName(u"input_image_failed_quantity")
        self.input_image_failed_quantity.setReadOnly(True)

        self.gridLayout_5.addWidget(self.input_image_failed_quantity, 0, 5, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_5.addWidget(self.label_3, 0, 4, 1, 1)

        self.input_total_quantity = QLineEdit(self.groupBox_2)
        self.input_total_quantity.setObjectName(u"input_total_quantity")
        self.input_total_quantity.setReadOnly(True)

        self.gridLayout_5.addWidget(self.input_total_quantity, 0, 1, 1, 1)

        self.input_repeat_quantity = QLineEdit(self.groupBox_2)
        self.input_repeat_quantity.setObjectName(u"input_repeat_quantity")
        self.input_repeat_quantity.setReadOnly(True)

        self.gridLayout_5.addWidget(self.input_repeat_quantity, 0, 7, 1, 1)


        self.gridLayout_9.addWidget(self.groupBox_2, 2, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_7 = QGridLayout(self.groupBox_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.textarea_log = QTextEdit(self.groupBox_3)
        self.textarea_log.setObjectName(u"textarea_log")
        self.textarea_log.setReadOnly(True)

        self.gridLayout_7.addWidget(self.textarea_log, 1, 0, 1, 1)

        self.button_clear_log = QPushButton(self.groupBox_3)
        self.button_clear_log.setObjectName(u"button_clear_log")

        self.gridLayout_7.addWidget(self.button_clear_log, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.groupBox_3, 3, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")

        self.gridLayout_6.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1105, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"scrapy \u6570\u636e\u5bfc\u51fa\u5de5\u5177", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8fc7\u6ee4", None))
        self.input_filter_min_price.setText(QCoreApplication.translate("MainWindow", u"1.00", None))
        self.checkbox_filter_repeat_sku_product.setText(QCoreApplication.translate("MainWindow", u"\u8fc7\u6ee4\u91cd\u590dsku\u4ea7\u54c1", None))
        self.checkbox_filter_invalidate_product.setText(QCoreApplication.translate("MainWindow", u"\u8fc7\u6ee4\u65e0\u6548\u4ea7\u54c1", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u8fc7\u6ee4\u6700\u4f4e\u4ef7\u683c", None))
        self.button_check_data.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u67e5", None))
        self.check_box_filter_image.setText(QCoreApplication.translate("MainWindow", u"\u8fc7\u6ee4\u56fe\u7247\u4e0b\u8f7d\u5931\u8d25\u7684\u4ea7\u54c1", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d", None))
        self.button_load_project.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u9879\u76ee\u6587\u4ef6(excel)", None))
        self.button_set_default_brand.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u9ed8\u8ba4\u54c1\u724c", None))
        self.label_project_file.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u6570\u636e", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u590d\u6570\u636e\u6570", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u603b\u8bb0\u5f55\u6570", None))
        self.button_export_data.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u7b5b\u9009\u540e\u8bb0\u5f55\u6570", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u4e0b\u8f7d\u5931\u8d25\u6570", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u65e5\u5fd7", None))
        self.button_clear_log.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7a7a\u65e5\u5fd7", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u64cd\u4f5c", None))
    # retranslateUi

