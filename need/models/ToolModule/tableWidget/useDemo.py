import sys

from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QApplication

from tableWidget_freeze import Freeze


class MainShowTable(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.main_layout = QGridLayout(self)
        self.tw = QTableWidget()
        
        self.freeze = Freeze(self.tw, 4, 3, use_row_sub_scroll=True)
        
        self.main_layout.addWidget(self.tw, 0, 0, 5, 5)
        self.resize(640, 480)
        self.setFont(QFont('微软雅黑', 7))
        
        self.tw.setColumnCount(100)
        self.tw.setRowCount(100)
        
        # 设置格大小
        self.tw.horizontalHeader().setDefaultSectionSize(50)
        self.tw.verticalHeader().setDefaultSectionSize(50)
        
        # 将自带的滑动条禁用     1 -》Qt.ScrollBarAlwaysOff 2-》Qt.ScrollBarAlwaysOn
        self.tw.setVerticalScrollBarPolicy(1)
        self.tw.setHorizontalScrollBarPolicy(1)
        
        # 设置从冻结行列获取的横纵滑动条的位置
        self.main_layout.addWidget(self.freeze.horizon, 5, 0, 1, 5)
        self.main_layout.addWidget(self.freeze.vertical, 0, 5, 5, 1)
        
        # 渲染tableWidget数据
        row_count = self.tw.rowCount()
        col_count = self.tw.columnCount()
        for row in range(row_count):
            for col in range(col_count):
                item = QTableWidgetItem(f'{row}-{col}')
                color = (int(255 - row / row_count * 255),
                         int(255 - col / col_count * 255),
                         int(255 - (col + row) / (row_count + col_count) * 255))
                item.setBackground(QColor(*color))
                item.setText(f'#{hex(color[0])[2:]}{hex(color[1])[2:]}{hex(color[2])[2:]}')
                self.tw.setItem(row, col, item)
    
    # 重新设置冻结的横纵范围
    def reFreezeRange(self):
        self.freeze.reSet()


MainWidget = MainShowTable

if __name__ == '__main__':
    """
    Main run
    """
    
    app = QApplication(sys.argv)
    
    ui = MainShowTable()
    ui.show()
    ui.reFreezeRange()
    sys.exit(app.exec_())
