# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerjOPmqe.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import sys
import traceback

from PyQt5.QtCore import QCoreApplication, QMetaObject
from PyQt5.QtWidgets import (QApplication, QDialog, QFormLayout, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QSizePolicy,
                             QSpacerItem, QMessageBox)

# class Ui_Dialog(object):
#     def setupUi(self, Dialog):
#         if not Dialog.objectName():
#             Dialog.setObjectName(u"Dialog")
#         Dialog.resize(400, 300)
#         self.gridLayout = QGridLayout(Dialog)
#         self.gridLayout.setObjectName(u"gridLayout")
#         self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
#
#         self.gridLayout.addItem(self.verticalSpacer, 0, 2, 1, 1)
#
#         self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
#
#         self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)
#
#         self.formLayout = QFormLayout()
#         self.formLayout.setObjectName(u"formLayout")
#         self.label = QLabel(Dialog)
#         self.label.setObjectName(u"label")
#
#         self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)
#
#         self.le_user = QLineEdit(Dialog)
#         self.le_user.setObjectName(u"le_user")
#         sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.le_user.sizePolicy().hasHeightForWidth())
#         self.le_user.setSizePolicy(sizePolicy)
#
#         self.formLayout.setWidget(0, QFormLayout.FieldRole, self.le_user)
#
#         self.label_2 = QLabel(Dialog)
#         self.label_2.setObjectName(u"label_2")
#
#         self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)
#
#         self.le_passwd = QLineEdit(Dialog)
#         self.le_passwd.setObjectName(u"le_passwd")
#         sizePolicy.setHeightForWidth(self.le_passwd.sizePolicy().hasHeightForWidth())
#         self.le_passwd.setSizePolicy(sizePolicy)
#
#         self.formLayout.setWidget(1, QFormLayout.FieldRole, self.le_passwd)
#
#         self.gridLayout.addLayout(self.formLayout, 1, 1, 1, 2)
#
#         self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
#
#         self.gridLayout.addItem(self.horizontalSpacer_2, 1, 3, 1, 1)
#
#         self.pb_login = QPushButton(Dialog)
#         self.pb_login.setObjectName(u"pb_login")
#
#         self.gridLayout.addWidget(self.pb_login, 2, 1, 1, 2)
#
#         self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
#
#         self.gridLayout.addItem(self.verticalSpacer_2, 3, 1, 1, 1)
#
#         self.retranslateUi(Dialog)
#
#         QMetaObject.connectSlotsByName(Dialog)
#
#     # setupUi
#
#     def retranslateUi(self, Dialog):
#         Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
#         self.label.setText(QCoreApplication.translate("Dialog", u"\u8d26\u53f7", None))
#         self.label_2.setText(QCoreApplication.translate("Dialog", u"\u5bc6\u7801", None))
#         self.pb_login.setText(QCoreApplication.translate("Dialog", u"\u767b\u5f55", None))
#     # retranslateUi

from loginView import Ui_Dialog


view = None


def load_mainModule():
    try:
        from need.module import loader
        main_view = loader.get_module('main_view')
        return main_view
    except:
        traceback.print_exc()
        pass


class LoginView(QDialog, Ui_Dialog):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        
        self.pb_login.clicked.connect(self.login)
    
    def login(self):
        user = self.le_user.text()
        passwd = self.le_passwd.text()
        if user == 'admin' and passwd == '123456':
            self.accept()


# 启动加载项
def start_boot():
    login = LoginView()
    if login.exec_() == login.Accepted:
        
        try:
            main_view = load_mainModule()
            if main_view:
                global view
                view = main_view.MainView()
                view.show()
            else:
                return QMessageBox.information(None, '提示', '主模块不存在')
        except:
            
            return QMessageBox.information(None, '提示', '主模块加载失败')


if __name__ == '__main__':
    """
    Main run
    """
    
    app = QApplication(sys.argv)
    
    # ui = LoginView()
    # ui.show()
    start_boot()
    sys.exit(app.exec_())
