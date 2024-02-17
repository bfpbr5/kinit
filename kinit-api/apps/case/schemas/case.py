#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/02/15 18:43
# @File           : case.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DateStr, DatetimeStr


class Case(BaseModel):
    name: str = Field(..., title="案件名称")
    case_datetime: DateStr = Field(..., title="案件时间")
    case_file: str | None = Field(None, title="案情描述文件")
    desc: str | None = Field(None, title="案情描述")
    cause: str | None = Field(None, title="案由")
    claim: str | None = Field(None, title="诉讼请求")
    timeline: str | None = Field(None, title="时间线")
    relation: str | None = Field(None, title="案情综述")
    questions: str | None = Field(None, title="待澄清问题")


class CaseSimpleOut(Case):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
