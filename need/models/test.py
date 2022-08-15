import sys
import traceback

# from PyQt5.Qt import *
from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton, QMessageBox, QApplication

from need.module import loader


# 下面的设置不利于动态加载，当重新加载test_1模块时 如果使用下面的操作，那么当前模块也需要重新加载才可以加载新的test_1
# try:
#     if setting.debug:
#         import test_1
#     else:
#         test_1 = loader.get_module('test_1')
# except:
#     traceback.print_exc()
#     test_1 = loader.get_module('test_1')


# def reload(name):
#     def fn_run(fn):
#         if name:
#             loader.reload_module(name)
#         else:
#
#             pass
#
#         @functools.wraps(fn)
#         def run(*args, **kwargs):
#             return fn(*args, **kwargs)
#
#         return run
#
#     return fn_run


class MainUi(QDialog):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.resize(320, 240)
        self.start()
        pb = QPushButton('显示test1!', self)
        pb.clicked.connect(self.show_test1)
    
    def start(self):
        pass
    
    def show_test1(self):
        test_1 = loader.get_module('test_1')
        
        if test_1:
            a = test_1.MainUi()
            a.exec_()
        else:
            QMessageBox.information(self, '提示', '模块加载失败')


MainWidget = MainUi

if __name__ == '__main__':
    """
    Main run
    直接用cython打包成pyd也可以直接使用
    """
    
    app = QApplication(sys.argv)
    
    ui = MainUi()
    ui.show()
    
    sys.exit(app.exec_())
