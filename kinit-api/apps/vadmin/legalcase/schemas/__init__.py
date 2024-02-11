#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/10/19 15:41 
# @File           : __init__.py.py
# @IDE            : PyCharm
# @desc           : 简要说明

import pkgutil
import importlib

# 遍历当前目录中的所有模块
for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
    # 跳过本文件（__init__.py）
    if module_name == '__init__':
        continue
    # 导入模块
    module = importlib.import_module('.' + module_name, __package__)
    # 遍历模块中的所有属性
    for attribute_name in dir(module):
        # 获取属性的值（可能是一个类或其他对象）
        attribute = getattr(module, attribute_name)
        # 检查属性是否是一个类，并且确保它不是本模块中定义的
        # 同时检查类名和限定名是否相同，以忽略嵌套的类
        if (isinstance(attribute, type) and 
            attribute.__module__ == module.__name__ and 
            attribute.__name__ == attribute.__qualname__):
            # 将类导出到当前命名空间
            globals()[attribute_name] = attribute