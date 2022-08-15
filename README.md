# DemoLoadModule

本项目是一个测试模块加载的一个demo，仅本地测试可用

主要是用于对pyd进行动态管理和加载。
## 示例1：
[![vazpy8.gif](https://s1.ax1x.com/2022/08/15/vazpy8.gif)](https://imgtu.com/i/vazpy8)
## 示例2：
[![vdF4KI.gif](https://s1.ax1x.com/2022/08/15/vdF4KI.gif)](https://imgtu.com/i/vdF4KI)
## main.py

    main.py 是一个示例可导入文件，可以直接运行或者打包成exe文件。
    将pyd拖拽到窗口，将添加或者更新pyd的模块。

```python
import need.setting         # 导入一个设置文件 必须！因为这个文件将设置模块存放位置和sqlite.db存放位置

```
setting.py

```python
# setting.py

RelativePath = '../'    # 相对于根目录的路径, 可以将文件存放在根目录

DBName = 'test'         # 数据库的名字


argv1 = sys.argv[0]

module_path = ''        # 当是debug时 sys.path.append(module_path) 方便调用


# 判断当前运行环境是否是py运行
if 'python' in argv1.lower() or Path(argv1).suffix in ['.py', '.pyd']:
    debug = True
    sys.path.append(module_path)
else:
    debug = False

```

```python
from need.module import load_module

load_module.instance()  # 将modules实例化
modules = load_module.modules   # 获取modules
```

modules 是一个管理模块的对象
```python

from need.module import load_module

load_module.instance()          # 将modules实例化
modules = load_module.modules   # 获取modules
file = r'need/models/b_build/test.pyd'
test = modules.append(file)     # 通过文件添加模块
# test = modules.update_module(file)     # 通过文件添加模块

# test = modules['test']        # 通过名称获取模块

start_boot = modules.setting['start_boot']      # 获取模块设置的标签对象，存放模块名称
start_boot += test                              # 添加该标签的模块
start_boot -= test                              # 删除该标签的模块
start_boot_first_item = start_boot.o            # 获取该标签的首个模块名

```

modules.setting可以进行标签设置
例: 
```python
start_boot = modules.setting['start_boot']      # 获取模块设置的标签对象，存放模块名称
start_boot += test                              # 添加该标签的模块
start_boot -= test                              # 删除该标签的模块
start_boot_first_item = start_boot.o            # 获取该标签的首个模块名
```

## need/models/test.py

测试用例 test.py
```python
from need.module import loader          # 导入加载器

test_1 = loader.get_module('test_1')    # 获取模块test_1 return：module/None

```
    
    
    

