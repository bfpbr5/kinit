#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/02/15 18:43
# @File           : case.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DateStr, DatetimeStr


class ChainOfEvidence(BaseModel):
    case_id: int = Field(..., title="关联案件")
    content: str = Field(..., title="证据内容")
    file_url: str | None = Field(None, title="证据上传文件")
    upload_status: bool = Field(False, title="是否已上传文件")


class ChainOfEvidenceSimpleOut(ChainOfEvidence):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
