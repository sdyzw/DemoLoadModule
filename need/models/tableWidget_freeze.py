import sys

from PyQt5.Qt import *


class Freeze():
    
    def __init__(self, tw: QTableWidget, row=0, col=0, *args, **kwargs):
        super().__init__()
        self.tw = tw
        self.horizon = QScrollBar(Qt.Horizontal)
        self.vertical = QScrollBar(Qt.Vertical)
        self.hor_val = 0
        self.ver_val = 0
        self.fre_row = 0
        self.fre_col = 0
        
        self.hor_hide_list = []
        self.hor_hide_start = 0
        
        self.ver_hide_list = []
        self.ver_hide_start = 0
        
        self.horizon.valueChanged.connect(self.hor_value_change)
        self.vertical.valueChanged.connect(self.ver_value_change)
        self.tw.horizontalScrollBar().valueChanged.connect(self.tw_hor_value_change)
        self.tw.verticalScrollBar().valueChanged.connect(self.tw_ver_value_change)
        self.set_freezeCol(col)
        self.set_freezeRow(row)
        # self.tw.horizontalScrollBar().rangeChanged.connect(self.hor_range_change)
        # self.tw.verticalScrollBar().rangeChanged.connect(self.ver_range_change)
        # self.horizon.setRange(self.tw.horizontalScrollBar().minimum(), self.tw.horizontalScrollBar().maximum())
        # self.horizon.setRange(self.tw.horizontalScrollBar().minimum(), 5)
        # self.vertical.setRange(self.tw.verticalScrollBar().minimum(), self.tw.verticalScrollBar().maximum())
        # self.vertical.setRange(self.tw.verticalScrollBar().minimum(), 4)
        # self.tw.horizontalScrollBar().rangeChanged.connect(self.horizon.setRange)
        # self.tw.verticalScrollBar().rangeChanged.connect(self.vertical.setRange)
    
    def hor_value_change(self, p_int):
        if not (self.fre_col and isinstance(self.fre_col, int) and self.fre_col > 0):
            self.tw.horizontalScrollBar().setValue(p_int)
            return
        if p_int > self.hor_val:  # ->
            for i in range(self.hor_val + 1, p_int + 1):
                self.tw.setColumnHidden(self.hor_hide_start, True)
                self.hor_hide_list.append(self.hor_hide_start)
                self.hor_hide_start += 1
        elif p_int < self.hor_val:  # <-
            for i in range(p_int, self.hor_val):
                self.hor_hide_start = self.hor_hide_list.pop(-1)
                self.tw.setColumnHidden(self.hor_hide_start, False)
        
        self.hor_val = p_int
    
    def ver_value_change(self, p_int):
        if not (self.fre_row and isinstance(self.fre_row, int) and self.fre_row > 0):
            self.tw.verticalScrollBar().setValue(p_int)
            return
        
        if p_int > self.ver_val:  # ->
            for i in range(self.ver_val, p_int):
                self.tw.setRowHidden(self.ver_hide_start, True)
                self.ver_hide_list.append(self.ver_hide_start)
                self.ver_hide_start += 1
        elif p_int < self.ver_val:  # <-
            for i in range(p_int, self.ver_val):
                self.ver_hide_start = self.ver_hide_list.pop(-1)
                self.tw.setRowHidden(self.ver_hide_start, False)
        # print(self.ver_val, self.ver_hide_start, self.ver_hide_list)
        self.ver_val = p_int
    
    def tw_hor_value_change(self, p_int):
        if not p_int:
            return
        self.horizon.setSliderPosition(self.hor_val + p_int)
        self.tw.horizontalScrollBar().setSliderPosition(0)
    
    def tw_ver_value_change(self, p_int):
        if not p_int:
            return
        self.vertical.setSliderPosition(self.ver_val + p_int)
        self.tw.verticalScrollBar().setSliderPosition(0)
    
    def reSet(self):
        # self.horizon.setRange(self.tw.horizontalScrollBar().minimum(), self.tw.horizontalScrollBar().maximum())
        # self.vertical.setRange(self.tw.verticalScrollBar().minimum(), self.tw.verticalScrollBar().maximum())
        # print(self.tw.horizontalScrollBar().minimum(), self.tw.horizontalScrollBar().maximum())
        # print(self.tw.verticalScrollBar().minimum(), self.tw.verticalScrollBar().maximum())
        self.horizon.setRange(self.tw.horizontalScrollBar().minimum(), self.tw.horizontalScrollBar().maximum())
        self.vertical.setRange(self.tw.verticalScrollBar().minimum(), self.tw.verticalScrollBar().maximum())
        # print(self.horizon.maximum(), self.vertical.maximum())
    
    def set_freezeRow(self, p_int: int):
        if not isinstance(p_int, int):
            return
        if self.ver_hide_list:
            return QMessageBox.information(None, '提示', '当前冻结行正在使用中，请恢复正常后进行设置')
        
        if p_int > 0:
            self.fre_row = p_int
            self.ver_hide_start = p_int
        else:
            self.fre_row = 0
            self.ver_hide_start = 0
    
    def set_freezeCol(self, p_int: int):
        if not isinstance(p_int, int):
            return
        if self.hor_hide_list:
            return QMessageBox.information(None, '提示', '当前冻结列正在使用中，请恢复正常后进行设置')
        
        if p_int > 0:
            self.fre_col = p_int
            self.hor_hide_start = p_int
        else:
            self.fre_col = 0
            self.hor_hide_start = 0


class MainShowTable(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.main_layout = QGridLayout(self)
        self.tw = QTableWidget()
        
        self.freeze = Freeze(self.tw, 4, 3)
        self.main_layout.addWidget(self.tw, 0, 0, 5, 5)
        self.resize(640, 480)
        
        self.tw.setColumnCount(100)
        self.tw.setRowCount(100)

        # 将自带的滑动条禁用
        self.tw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.tw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.tw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        self.main_layout.addWidget(self.freeze.horizon, 5, 0, 1, 5)
        self.main_layout.addWidget(self.freeze.vertical, 0, 5, 5, 1)
        
        for row in range(self.tw.rowCount()):
            for col in range(self.tw.columnCount()):
                self.tw.setItem(row, col, QTableWidgetItem(f'{row}-{col}'))
    
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
