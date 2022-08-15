import sys
from pathlib import Path

RelativePath = '../'    # 相对于根目录的路径

DBName = 'test'


argv1 = sys.argv[0]

module_path = ''        # 当是debug时 sys.path.append(module_path) 方便调用


if 'python' in argv1.lower() or Path(argv1).suffix in ['.py', '.pyd']:
    debug = True
    sys.path.append(module_path)
else:
    debug = False
