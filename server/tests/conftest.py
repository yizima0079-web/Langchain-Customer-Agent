"""pytest 公共配置：将 server/ 根目录加入 sys.path，使 app 包可导入。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
