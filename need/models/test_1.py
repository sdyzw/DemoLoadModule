import sys

from PyQt5.Qt import *


class MainUi(QDialog):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.resize(160, 120)
        self.setWindowTitle('我是test66666')
        self.start()
        
        label = QLabel('我是test', self, )
    
    def start(self):
        pass


if __name__ == '__main__':
    """
    Main run
    直接用cython打包成pyd也可以直接使用
    """
    
    app  = QApplication(sys.argv)
    
    ui = MainUi()
    ui.show()
    
    sys.exit(app.exec_())
