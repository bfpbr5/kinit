'''
## 项目结构

使用的是仿照 Django 项目结构：

- alembic：数据库迁移配置目录
  - versions_dev：开发环境数据库迁移文件目录
  - versions_pro：生产环境数据库迁移文件目录
  - env.py：映射类配置文件
- application：主项目配置目录，也存放了主路由文件
  - config：基础环境配置文件
    - development.py：开发环境
    - production.py：生产环境
  - settings.py：主项目配置文件
  - urls.py：主路由文件
- apps：项目的app存放目录
  - vadmin：基础服务
    - auth：用户 - 角色 - 菜单接口服务
      - models：ORM 模型目录
      - params：查询参数依赖项目录
      - schemas：pydantic 模型，用于数据库序列化操作目录
      - utils：登录认证功能接口服务
      - curd.py：数据库操作
      - views.py：视图函数
- core：核心文件目录
  - crud.py：关系型数据库操作核心封装
  - database.py：关系型数据库核心配置
  - data_types.py：自定义数据类型
  - exception.py：异常处理
  - logger：日志处理核心配置
  - middleware.py：中间件核心配置
  - dependencies.py：常用依赖项
  - event.py：全局事件
  - mongo_manage.py：mongodb 数据库操作核心封装
  - validator.py：pydantic 模型重用验证器
- db：ORM模型基类
- logs：日志目录
- static：静态资源存放目录
- utils：封装的一些工具类目录
- main.py：主程序入口文件
- alembic.ini：数据库迁移配置文件


在典型的Web应用程序中，新功能模块的业务逻辑通常会分布在以下几个位置：

视图函数 (views.py)： 视图函数是处理HTTP请求的主要地点，在这里编写业务逻辑以及调用其他模块的功能。视图函数通常会处理请求参数、调用数据库操作、进行业务逻辑处理，并返回HTTP响应。

数据库操作 (curd.py, models.py)： 如果新功能模块涉及到与数据库的交互，那么数据库操作部分的业务逻辑会集中在curd文件或者models文件中。curd文件中通常包含对数据库的增删改查操作，而models文件则包含数据库模型定义以及模型间的关联等。

参数验证 (params)： 在处理HTTP请求时，通常需要对传入的参数进行验证和处理。参数验证的逻辑可以单独放置在params目录下，使用Pydantic等库来定义参数模型并进行验证。

其他工具类 (utils)： 新功能模块可能会涉及到一些通用的功能，例如身份认证、日志记录、文件操作等。相关的业务逻辑可以封装在工具类中，以便在视图函数或其他地方复用。

全局事件 (event.py)： 如果新功能模块需要与其他模块进行交互或者触发一些全局事件，可以在event.py中定义相关的事件处理逻辑。

中间件 (middleware.py)： 在处理HTTP请求和响应的过程中，可能需要进行一些预处理或者后处理的操作，这些操作可以放置在中间件中。

根据项目的实际需求和组织结构，以上位置中的一部分或者全部都可以用来编写新功能模块的业务逻辑。在开发过程中，良好的组织结构和代码规范能够提高代码的可读性和可维护性。


'''

# 下面是一个简单的Python类，用于封装添加新功能模块的流程

import os
import shutil

class NewModuleCreator:
    def __init__(self, module_name, base_directory):
        self.module_name = module_name
        self.base_directory = base_directory

    def create_module_structure(self):
        module_path = os.path.join(self.base_directory, "apps", self.module_name)
        os.makedirs(module_path, exist_ok=True)
        
        subdirectories = ["models", "params", "schemas", "utils"]
        for directory in subdirectories:
            os.makedirs(os.path.join(module_path, directory), exist_ok=True)
        
        open(os.path.join(module_path, "curd.py"), "w").close()
        open(os.path.join(module_path, "views.py"), "w").close()

        return module_path

    def add_to_settings(self):
        settings_path = os.path.join(self.base_directory, "application", "settings.py")
        with open(settings_path, "r") as f:
            lines = f.readlines()

        installed_apps_index = lines.index("INSTALLED_APPS = [\n") + 1
        lines.insert(installed_apps_index, f'    "application.apps.{self.module_name}",\n')

        with open(settings_path, "w") as f:
            f.writelines(lines)

    def add_to_urls(self):
        urls_path = os.path.join(self.base_directory, "application", "urls.py")
        with open(urls_path, "r") as f:
            content = f.read()

        new_router_import = f"from application.apps.{self.module_name} import views\n"
        new_router_include = f"router.include_router(views.router, prefix='/{self.module_name}', tags=['{self.module_name}'])\n"

        # Check if import statement already exists to avoid duplicates
        if new_router_import not in content:
            content += f"\n{new_router_import}"
        if new_router_include not in content:
            content += f"\n{new_router_include}"

        with open(urls_path, "w") as f:
            f.write(content)

    def create(self):
        module_path = self.create_module_structure()
        self.add_to_settings()
        self.add_to_urls()
        return module_path


def main():
    # Example usage:
    creator = NewModuleCreator("my_feature", "/path/to/project")
    new_module_path = creator.create()
    print(f"New module created at: {new_module_path}")


if __name__ == "__main__":
    main()
