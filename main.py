import logging
import sys
import traceback
import warnings

from PyQt5 import QtGui
from PyQt5.Qt import *

import need.setting

from need.module import load_module
from need.module.base_file import get_all_file_list

# from need.module.load_module import modules, instance


load_module.instance()
modules = load_module.modules


class MainUi(QWidget):
    load_signal = pyqtSignal(list)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.setAcceptDrops(True)
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
            try:
                if hasattr(module, "run"):
                    module.run()
                if hasattr(module, "MainWidget"):       # 添加主加载界面 &尽量设置为一个
                    main_widget = module.MainWidget
                    # main_setting = modules.setting['main']
                    modules.setting['main'] += module
                    if issubclass(main_widget, QWidget):
                        main_ = main_widget()
                        self.main_layout.addWidget(main_)
                if hasattr(module, "MainWidget__", ) and module.MainWidget__:     # 删除当前模块的主加载界面
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
    
    def start_bootItem(self, ):
        """
        启动加载项
        :return:
        """
        if modules.setting['main'].o:
            module = modules[modules.setting['main'].o]
            if module:
                try:
                    main_widget = module.MainWidget
                    # modules.setting['main'] += module
                    if issubclass(main_widget, QWidget):
                        main_ = main_widget()
                        self.main_layout.addWidget(main_)
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


def test():         # 使用loader来获取 模块管理的实例化对象
    from need.module import loader
    modules_manage = loader.get_modules_manage()        # 模块管理对象
    
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
