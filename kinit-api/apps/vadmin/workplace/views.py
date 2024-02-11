#!/usr/bin/python
# -*- coding: utf-8 -*-
# JG_EDIT



from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter
from utils.response import SuccessResponse

import datetime


app = APIRouter()


###########################################################
#    工作区管理
###########################################################

# ==================以下为旧代码=====================
@app.get("/case_info", summary="获取案件列表")
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
