import time

a_time = time.time()
import sys

sys.path.append('')
print(time.time() - a_time)

# from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget

print(time.time() - a_time)
from PyQt5.QtWidgets import QApplication

print(time.time() - a_time)

from ui_module_manage import Ui_Form

print(time.time() - a_time)


class VModuleManage(QWidget, Ui_Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)


if __name__ == '__main__':
    """
    Main run
    """
    
    app = QApplication(sys.argv)
    a_time1 = time.time()
    ui = VModuleManage()
    print(time.time() - a_time1, '初始化')
    a_time1 = time.time()
    ui.show()
    print(time.time() - a_time1, '显示')
    print(time.time() - a_time)
    sys.exit(app.exec_())
