# 1，QTableWidget 冻结行列

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

### 原理（以下以列冻结做说明（冻结3列），行同理）

freeze提供了横纵滑动条（以下简称：新滑动条），新滑动条需要和QTableWidget（以下简称：tw）的横纵滑动条（以下简称：旧滑动条）的区间一样，
这样新滑动条可以确保和旧滑动条的滑动长度是一样的，以方便进行滑动同步。 


1，当新滑动条进行移动时：新滑动条将在视觉上替代旧滑动条，当新滑动条向右滑动时，意味着冻结列的下一列将滑到冻结列的位置，此处将下一列隐藏起来作为冻结列向左滑动的结果，所以当滑动条每向右滑动时，冻结列的下一列都将做隐藏处理，这样得到的结果就是
列从 123456789 -》 12356789 -》1236789 -》 123789，展示效果就是 滑动条向右滑动，没有冻结的 456789在向左运动，由456789-》56789-》6789。由此做出冻结列的效果。同理当滑动条向左滑动时，冻结列当前被隐藏的最后一个进行解除隐藏。。。

2，当tw自身的进行滑动条移动时，由于要确保冻结列的形成，所以将固定旧滑动条永远处于开始端，当旧滑动条向右滑动时，通过事件valueChanged获取，然后将旧滑动条setSliderPosition(0)，这样就确保冻结的列时冻结的状态，同时将新滑动条移动相同的距离，
可视为移动旧滑动条就是移动新滑动条且复位旧滑动条。
