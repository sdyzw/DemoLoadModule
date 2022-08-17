import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QTableWidget, QScrollBar, QMessageBox, QWidget, QGridLayout, QTableWidgetItem, QApplication


class MyVerticalScrollBar(QScrollBar):
    upSignal = pyqtSignal()
    downSignal = pyqtSignal()
    
    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        y = a0.angleDelta().y()
        # print(a0.angleDelta())
        if y == -120:
            self.downSignal.emit()
        elif y == 120:
            self.upSignal.emit()


# tableWidget冻结行列
class Freeze:
    _horizon = None
    _vertical = None
    
    def __init__(self, tw: QTableWidget, row=0, col=0, horizon: QScrollBar = None, vertical: QScrollBar = None,
                 use_row_sub_scroll=False,
                 *args,
                 **kwargs):
        super().__init__()
        self.tw = tw
        
        self.hor_freeze_flag = None
        self.ver_freeze_flag = None
        
        self.hor_val = 0  # 当前横向滑块的位置
        self.ver_val = 0  # 当前纵向滑块的位置
        
        self.hor_hide_list = []  # 横向已经隐藏的列的列表
        self.hor_hide_start = 0  # 横向下一个隐藏的开始索引
        
        self.ver_hide_list = []  # 纵向已经隐藏的行的列表
        self.ver_hide_start = 0  # 纵向下一个隐藏的开始索引
        
        self.set_freezeCol(col, horizon)
        self.set_freezeRow(row, vertical)
        
        if use_row_sub_scroll:  # 使用vertical附加滑动条，不使用则滚轮无法进行正常的向上滑动
            sub_verScrollBar = MyVerticalScrollBar()
            self.tw.setVerticalScrollBar(sub_verScrollBar)
            sub_verScrollBar.upSignal.connect(self.up)
            sub_verScrollBar.downSignal.connect(self.down)
        
        self.tw.horizontalScrollBar().valueChanged.connect(self.tw_hor_value_change)
        self.tw.verticalScrollBar().valueChanged.connect(self.tw_ver_value_change)
    
    @property
    def horizon(self) -> QScrollBar:
        if not self._horizon:
            self.horizon = QScrollBar(1)  # 1-》Qt.Horizontal
        return self._horizon
    
    @horizon.setter
    def horizon(self, scrollBar):
        self._horizon = scrollBar
        if self._horizon and isinstance(self._horizon, QScrollBar):
            self._horizon.valueChanged.connect(self.hor_value_change)
    
    @property
    def vertical(self) -> QScrollBar:
        if not self._vertical:
            self.vertical = QScrollBar(2)  # 2-》Qt.Vertical
        return self._vertical
    
    @vertical.setter
    def vertical(self, scrollBar):
        self._vertical = scrollBar
        if self._vertical and isinstance(self._vertical, QScrollBar):
            self._vertical.valueChanged.connect(self.ver_value_change)
    
    def hor_value_change(self, p_int):  # 横向滚动 滑块向左移动就逐个隐藏，向右移动就逐个将隐藏的显示
        if not self.hor_freeze_flag:
            return self.tw.horizontalScrollBar().setValue(p_int)
        
        if p_int > self.hor_val:  # ->
            for i in range(self.hor_val, p_int):
                self.tw.setColumnHidden(self.hor_hide_start, True)
                self.hor_hide_list.append(self.hor_hide_start)
                self.hor_hide_start += 1
        elif p_int < self.hor_val:  # <-
            for i in range(p_int, self.hor_val):
                self.hor_hide_start = self.hor_hide_list.pop(-1)
                self.tw.setColumnHidden(self.hor_hide_start, False)
        self.hor_val = p_int
    
    def ver_value_change(self, p_int):  # 纵向滚动 滑块向下移动就逐个隐藏，向上移动就逐个将隐藏的显示
        if not self.ver_freeze_flag:
            return self.tw.verticalScrollBar().setValue(p_int)
        
        if p_int > self.ver_val:  # ->
            for i in range(self.ver_val, p_int):
                self.tw.setRowHidden(self.ver_hide_start, True)
                self.ver_hide_list.append(self.ver_hide_start)
                self.ver_hide_start += 1
        elif p_int < self.ver_val:  # <-
            for i in range(p_int, self.ver_val):
                self.ver_hide_start = self.ver_hide_list.pop(-1)
                self.tw.setRowHidden(self.ver_hide_start, False)
        self.ver_val = p_int
    
    def tw_hor_value_change(self, p_int):  # 本身的滑块滑动：将值设置为0，且将附加的滑块加上对应的值
        if p_int:
            self.horizon.setSliderPosition(self.hor_val + p_int)
            self.tw.horizontalScrollBar().setSliderPosition(0)
    
    def tw_ver_value_change(self, p_int):  # 本身的滑块滑动：将值设置为0，且将附加的滑块加上对应的值
        if p_int:
            self.vertical.setSliderPosition(self.ver_val + p_int)
            self.tw.verticalScrollBar().setSliderPosition(0)
    
    def down(self):
        self.vertical.triggerAction(QScrollBar.SliderAction.SliderSingleStepAdd)
    
    def up(self):
        self.vertical.triggerAction(QScrollBar.SliderAction.SliderSingleStepSub)
    
    def reSet(self):  # 重新设置横纵滑块区间：range
        if self.horizon:
            self.horizon.setMaximum(self.tw.horizontalScrollBar().maximum())
        if self.vertical:
            self.vertical.setMaximum(self.tw.verticalScrollBar().maximum())
    
    def set_freezeRow(self, p_int: int, scrollBar=None):  # 设置冻结行
        if not isinstance(p_int, int):
            return
        if self.ver_hide_list:
            return QMessageBox.information(None, '提示', '当前冻结行正在使用中，请恢复正常后进行设置')
        self.ver_freeze_flag = p_int > 0
        self.ver_hide_start = p_int
        if scrollBar:
            self.reload_verticalScroll(scrollBar)
    
    def set_freezeCol(self, p_int: int, scrollBar=None):  # 设置冻结列
        if not isinstance(p_int, int):
            return
        if self.hor_hide_list:
            return QMessageBox.information(None, '提示', '当前冻结列正在使用中，请恢复正常后进行设置')
        self.hor_freeze_flag = p_int > 0
        self.hor_hide_start = p_int
        if scrollBar:
            self.reload_horizonScroll(scrollBar)
    
    def reload_horizonScroll(self, scrollBar: QScrollBar):  # 重新加载横向滑动条,是正常的scrollBar就成立，否则就重新设置一个
        self.horizon = scrollBar
    
    def reload_verticalScroll(self, scrollBar: QScrollBar):  # 重新加载纵向滑动条,是正常的scrollBar就成立，否则就重新设置一个
        self.vertical = scrollBar


class MainShowTable(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.main_layout = QGridLayout(self)
        self.tw = QTableWidget()
        
        self.freeze = Freeze(self.tw, 4, 3, use_row_sub_scroll=True)
        self.main_layout.addWidget(self.tw, 0, 0, 5, 5)
        self.resize(640, 480)
        self.setFont(QFont('微软雅黑', 7))
        
        self.tw.setColumnCount(255)
        self.tw.setRowCount(255)
        
        # 设置格大小
        self.tw.horizontalHeader().setDefaultSectionSize(50)
        self.tw.verticalHeader().setDefaultSectionSize(50)
        
        # 将自带的滑动条禁用     1 -》Qt.ScrollBarAlwaysOff 2-》Qt.ScrollBarAlwaysOn
        self.tw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
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
