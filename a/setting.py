import sys
from pathlib import Path

RelativePath = '../'    # 相对于根目录的路径

DBName = 'test'


argv1 = sys.argv[0]

if 'python' in argv1.lower() or Path(argv1).suffix in ['.py', '.pyd']:
    debug = True
else:
    debug = False
