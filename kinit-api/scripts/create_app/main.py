#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/12/9 15:27 
# @File           : main.py
# @IDE            : PyCharm
# @desc           : 简要说明
import datetime
import os.path

from application.settings import BASE_DIR


class CreateApp:

    APPS_ROOT = os.path.join(BASE_DIR, "apps")
    SCRIPT_DIR = os.path.join(BASE_DIR, 'scripts', 'create_app')

    def __init__(self, path: str):
        """
        :param path: app 路径，根目录为apps，填写apps后面路径即可，例子：vadmin/auth
        """
        self.app_path = os.path.join(self.APPS_ROOT, path)
        self.path = path

    def run(self):
        """
        自动创建初始化 APP 结构，如何该路径已经存在，则不执行
        """
        if self.exist(self.app_path):
            print(f"{self.app_path} 已经存在，无法自动创建，请删除后，重新执行。")
            return False
        print("开始生成 App 目录：", self.path)
        path = []
        for item in self.path.split("/"):
            path.append(item)
            self.create_pag(os.path.join(self.APPS_ROOT, *path))
        self.create_pag(os.path.join(self.app_path, "models"))
        self.create_pag(os.path.join(self.app_path, "params"))
        self.create_pag(os.path.join(self.app_path, "schemas"))
        self.generate_file("views.py")
        self.generate_file("crud.py")
        print("App 目录生成结束", self.app_path)

    def create_pag(self, path: str) -> None:
        """
        创建 python 包

        :param path: 绝对路径
        """
        if self.exist(path):
            return
        os.makedirs(path)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        init_file_content = '''
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
                    globals()[attribute_name] = attribute'''
        params = {
            "create_datetime": now,
            "filename": "__init__.py",
            "desc": "初始化文件",
            "content": init_file_content
        }
        self.create_file(os.path.join(path, "__init__.py"), "init.py", **params)

    def generate_file(self, name: str) -> None:
        """
        创建文件
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = {
            "create_datetime": now,
        }
        self.create_file(os.path.join(self.app_path, name), name, **params)

    def create_file(self, filepath: str, name: str, **kwargs):
        """
        创建文件
        """
        with open(filepath, "w", encoding="utf-8") as f:
            content = self.__get_template(name)
            f.write(content.format(**kwargs))

    @classmethod
    def exist(cls, path) -> bool:
        """
        判断路径是否已经存在
        """
        return os.path.exists(path)

    def __get_template(self, name: str) -> str:
        """
        获取模板内容
        """
        template = open(os.path.join(self.SCRIPT_DIR, "template", name), 'r')
        content = template.read()
        template.close()
        return content

# if __name__ == '__main__':
#     CreateApp()