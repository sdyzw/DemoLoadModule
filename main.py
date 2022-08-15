import logging
import sys
import traceback
import warnings

from PyQt5 import QtGui
from PyQt5.Qt import *

import need.setting

from need.module.base_file import get_all_file_list

# from need.module.load_module import modules, instance

from need.module import load_module

load_module.instance()
modules = load_module.modules


class MainUi(QWidget):
    load_signal = pyqtSignal(list)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.setAcceptDrops(True)
        self.load_list = {}
        self.mainWidget_update_show = True
        self.click_widget = None
        self.start()
    
    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        file = a0.mimeData().text()
        # print([file])
        files = get_all_file_list(file, need_suffix='pyd')
        '''check files'''
        QTimer.singleShot(100, lambda a=files: self.load_signal.emit(a))
    
    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        
        file = a0.mimeData().text()
        if not file:
            return
        a0.accept()
    
    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        print(a0.pos())
        a = self.childAt(a0.pos())
        if a != self:
            self.click_widget = a
    
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass
    
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.click_widget:
            drag = QDrag(self)
            data = QMimeData()
            pixmap = QPixmap(self.click_widget.size())
            self.click_widget.render(pixmap)

            drag.setMimeData(data)
            drag.setPixmap(pixmap)
            drag.setHotSpot(self.click_widget.mapFromGlobal(QCursor.pos()))
            self.click_widget: QWidget
            
            self.click_widget.setWindowOpacity(0)
            
            a = drag.exec_(Qt.MoveAction)
            point = self.mapToGlobal(self.mapFromGlobal(QCursor.pos()))
            pos = self.pos()
            size = self.size()
            if pos.x() <= point.x() <= pos.x() + size.width() and pos.y() <= point.y() <= pos.y() + size.height():
                self.click_widget.setWindowOpacity(1)
            else:
                name = None
                for name, widget in self.load_list.items():
                    if widget == self.click_widget:
                        break
                else:
                    QMessageBox.information(self, '提示', '当前模块查找失败')
                if name and QMessageBox.question(self, '提示', f'确认删除模块{name}') == QMessageBox.Yes:
                    modules.remove(name)
                    self.click_widget.setParent(None)
                    self.click_widget.setHidden(True)
                    self.click_widget.close()
                    self.main_layout.removeWidget(self.click_widget)
                    self.click_widget = None
                    self.load_list.pop(name, None)
                else:
                    self.click_widget.setWindowOpacity(1)

    def start(self):
        self.resize(640, 480)
        self.start_bootItem()
        self.load_signal.connect(self.load_modules)
    
    def load_modules(self, files):
        if not isinstance(files, list):
            return
        
        for module_file in files:
            module = modules.append(module_file)
            
            if not module:
                continue
            self.dispose_module(module)
            
    def dispose_module(self, module):
    
        # 以下为自定义内容 // 获取属性，当有该属性就进行什么操作 // 自定义属性 run，MainWidget，start_boot
        try:
            if hasattr(module, "run"):
                module.run()
        
            if hasattr(module, "MainWidget"):  # 添加主加载界面 &尽量设置为一个
                main_widget = module.MainWidget
                modules.setting['main'] += module
                self.load_mainWidget(module, main_widget)       # 加载显示mainWidget
        
            if hasattr(module, "MainWidget__", ) and module.MainWidget__:  # 删除当前模块的主加载界面
                modules.setting['main'] -= module
        except AttributeError:
            warnings.warn('当前没有run属性')
        except:
            traceback.print_exc()
    
        try:
            if hasattr(module, 'start_boot'):
                modules.setting['start_boot'] += module
            if hasattr(module, 'start_boot__') and module.start_boot__:
                modules.setting['start_boot'] -= module
        except:
            logging.info(f'当前模块启动加载项添加失败：{module}')
            
    def load_mainWidget(self, module, module_widget_class):
        module_name = module.__name__.split('.')[-1]
        if issubclass(module_widget_class, QWidget):
            if self.mainWidget_update_show and module_name in self.load_list:
                widget: QWidget = self.load_list.pop(module_name, None)
                try:
                    widget.close()
                except:
                    traceback.print_exc()
    
            if module_name not in self.load_list:
                main_ = module_widget_class()
                self.main_layout.addWidget(main_)
                self.load_list[module_name] = main_
        else:
            logging.warning('当前加载模块类型不为QWidget或已被加载过')
    
    def start_bootItem(self, ):
        """
        启动加载项
        :return:
        """
        # 只加载一项
        # if modules.setting['main'].o:
        #     module = modules[modules.setting['main'].o]
        #     if module:
        #         try:
        #             main_widget = module.MainWidget
        #             # modules.setting['main'] += module
        #             if issubclass(main_widget, QWidget):
        #                 main_ = main_widget()
        #                 self.main_layout.addWidget(main_)
        #         except:
        #             print('初始化模块加载失败')
        #             traceback.print_exc()
        
        # 拥有MainWidget属性的全部加载
        if modules.setting['main']:
            # module = modules[modules.setting['main'].o]
            for module_name in modules.setting['main']:
                module = modules[module_name]
                if module:
                    try:
                        main_widget = module.MainWidget
                        self.load_mainWidget(module, main_widget)
                    except:
                        print('初始化模块加载失败')
                        traceback.print_exc()
        
        start_boot = modules.setting['start_boot']
        for index, item in enumerate(start_boot):
            flag = False
            try:
                item = str(item)
                module = modules[item]
                if module and hasattr(module, 'start_boot'):
                    module.start_boot()
                    flag = True
                    print(f'{item}: 加载成功')
            except:
                print(f'{item}: 加载失败')
    
    def end_bootItem(self):
        
        pass


def test():  # 使用loader来获取 模块管理的实例化对象
    from need.module import loader
    modules_manage = loader.get_modules_manage()  # 模块管理对象
    
    pass


if __name__ == '__main__':
    """
    Main run
    nuitka --standalone --mingw64 --show-memory --show-progress --plugin-enable=qt-plugins  --include-qt-plugins=sensible,styles --follow-import-to=need,pywin32_bootstrap,winerror --output-dir="build"  "main.py" --nofollow-imports

    """
    
    app = QApplication(sys.argv)
    print(sys.argv)
    debug = 'debug' in sys.argv
    ui = MainUi()
    # if debug is True:  # 作为示例，当是debug环境显示界面
    #     ui.show()
    
    ui.show()
    sys.exit(app.exec_())
