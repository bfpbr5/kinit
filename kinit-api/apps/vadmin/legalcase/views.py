#!/usr/bin/python
# -*- coding: utf-8 -*-
# JG_EDIT



from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from core.database import db_getter
from utils.response import SuccessResponse
from . import schemas, crud, params, models
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import AllUserAuth, FullAdminAuth, OpenAuth
from apps.vadmin.auth.utils.validation.auth import Auth

import datetime


app = APIRouter()


###########################################################
#    工作区管理
###########################################################

@app.get("/case_info", summary="获取案件列表")
async def get_case_info(
        params: UserParams = Depends(),
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.list"]))
):
    model = models.VadminUser
    options = [joinedload(model.roles), joinedload(model.depts)]
    schema = schemas.UserOut
    datas, count = await crud.UserDal(auth.db).get_datas(
        **params.dict(),
        v_options=options,
        v_schema=schema,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@app.post("/case_info", summary="创建案件")
async def create_user(data: schemas.UserIn, auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.create"]))):
    return SuccessResponse(await crud.UserDal(auth.db).create_data(data=data))


@app.delete("/case_info", summary="批量删除案件", description="软删除，删除后清空所关联的角色")
async def delete_case_info(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.delete"]))):
    if auth.user.id in ids.ids:
        return ErrorResponse("不能删除当前登录案件")
    elif 1 in ids.ids:
        return ErrorResponse("不能删除超级管理员案件")
    await crud.UserDal(auth.db).delete_datas(ids=ids.ids, v_soft=True, is_active=False)
    return SuccessResponse("删除成功")


@app.put("/case_info/{data_id}", summary="更新案件信息")
async def put_user(
        data_id: int,
        data: schemas.UserUpdate,
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.update"]))
):
    return SuccessResponse(await crud.UserDal(auth.db).put_data(data_id, data))


@app.get("/case_info/{data_id}", summary="获取案件信息")
async def get_user(
        data_id: int,
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.view", "auth.user.update"]))
):
    model = models.VadminUser
    options = [joinedload(model.roles), joinedload(model.depts)]
    schema = schemas.UserOut
    return SuccessResponse(await crud.UserDal(auth.db).get_data(data_id, v_options=options, v_schema=schema))

# ==================以下为旧代码=====================
@app.get("/project", summary="获取案件列表")
async def get_project():
    data = [
        {
            "name": '租赁合同纠纷案',
            "icon": 'https://www.shoudu888.com/attachment/images/law/level_1.png',
            "message": '租客拖欠租金，房东要求解约索赔。',
            "personal": 'Bushi',
            "link": "https://www.mysql.com/",
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        },
        {
            "name": '离婚财产分割案',
            "icon": 'https://www.shoudu888.com/attachment/images/law/level_2.png',
            "message": '夫妻离婚，共同财产分割成焦点。',
            "personal": 'Bushi',
            "link": "https://fastapi.tiangolo.com/zh/",
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        },
        {
            "name": '劳动合同纠纷案',
            "icon": 'https://www.shoudu888.com/attachment/images/law/level_5.png',
            "message": '员工索要加班费及年假工资。',
            "personal": 'Bushi',
            "link": "https://cn.vuejs.org/",
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        },
        {
            "name": '交通事故损害赔偿案 ',
            "icon": 'https://www.shoudu888.com/attachment/images/law/level_8.png',
            "message": '行人车祸受伤，求偿医疗费等。',
            "personal": 'Bushi',
            "link": "https://element-plus.org/zh-CN/",
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        },
        {
            "name": '知识产权侵权案',
            "icon": 'https://www.shoudu888.com/attachment/images/law/level_6.png',
            "message": '软件著作权被侵犯，公司索赔。',
            "personal": 'Bushi',
            "link": "https://www.typescriptlang.org/",
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        },
        {
            "name": '建设工程施工合同纠纷案',
            "icon": 'https://www.shoudu888.com/attachment/images/law/level_1.png',
            "message": '工程延期，质量差，引发诉讼。',
            "personal": 'Bushi',
            "link": "https://cn.vitejs.dev/",
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        }
    ]
    return SuccessResponse(data)
# ==================以上为旧代码=====================

@app.get("/case_info/add/view/number/{data_id}", summary="更新常见案件查看次数+1")
async def issue_add_view_number(data_id: int, db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.IssueDal(db).add_view_number(data_id))


@app.get("/dynamic", summary="获取动态")
async def get_dynamic():
    data = [
        {
            "keys": ['受理', 'XXX离婚财产分割案'],
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        },
        {
            "keys": ['调解', '知识产权侵权案'],
            "time": datetime.datetime.now().strftime("%Y-%m-%d")
        }
    ]
    return SuccessResponse(data)


@app.get("/team", summary="获取团队信息")
async def get_team():
    data = [
        {
            "name": '张伟律师',
            "icon": 'vscode-icons:file-type-mysql'
        },
        {
            "name": '刘毅律师',
            "icon": 'logos:vue'
        },
        {
            "name": '王力宏律师',
            "icon": 'logos:element'
        },
        {
            "name": '齐春雷律师',
            "icon": 'simple-icons:fastapi'
        },
        {
            "name": '韦铭律师',
            "icon": 'vscode-icons:file-type-typescript-official'
        },
        {
            "name": '李杭律师',
            "icon": 'vscode-icons:file-type-vite'
        }
    ]
    return SuccessResponse(data)


@app.get("/shortcuts", summary="获取快捷操作")
async def get_shortcuts():
    data = [
        {
            "name": "中国裁判文书网",
            "link": "https://wenshu.court.gov.cn/"
        },
        {
            "name": "中国司法案例网",
            "link": "https://anli.court.gov.cn/"
        },
        {
            "name": "中国市场监管行政处罚文书网",
            "link": "http://cfws.samr.gov.cn/"
        },
        {
            "name": "中国审判流程信息公开网",
            "link": "https://splcgk.court.gov.cn/"
        },
        {
            "name": "中国庭审公开网",
            "link": "http://tingshen.court.gov.cn/"
        },
        {
            "name": "信用中国",
            "link": "https://www.creditchina.gov.cn/"
        },
    ]
    return SuccessResponse(data)
