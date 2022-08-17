# QTableWidget 冻结行列

## 示例：
[![vBRTaT.gif](https://s1.ax1x.com/2022/08/17/vBRTaT.gif)](https://imgtu.com/i/vBRTaT)

## tableWidget_freeze.py
    
```python
from tableWidget_freeze import Freeze
from PyQt5.QtWidgets import QTableWidget

tw = QTableWidget()
freeze = Freeze(tw, 4, 3, use_row_sub_scroll=True)
"""
渲染完数据之后
"""
freeze.reSet()          # 重新设置横纵滑块区间：range
```
所以就两句话完美解决QTableWidget的行列冻结

不过....要将freeze的行列给取出来作为QTableWidget的伪横纵滑块，因为自身携带的横纵滑块不能直接用新的来替代，
如果直接替代将会彻底影响QTableWidget的冻结以及滑动
```python
horizon = freeze.horizon
vertical = freeze.vertical
# 将QTableWidget自带的横纵滑动条设置为一直不显示
tw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
tw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

# 然后将horizon,vertical放置在合适的位置上即可替代原有的进行滑动
...

```

### freeze相关函数使用
```python
freeze = Freeze()
# 重新设置横纵滑块区间：range，用于表格大小（rowCount，columnCount）产生变化
freeze.reSet()      
# 设置冻结列，可以重新设置滑动条
freeze.set_freezeCol(int, scrollBar=None)
# 设置冻结行，可以重新设置滑动条
freeze.set_freezeRow(int, scrollBar=None)  
```