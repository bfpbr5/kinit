#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# JG_EDIT



from typing import Optional
from pydantic import BaseModel, ConfigDict
from core.data_types import DatetimeStr
from apps.vadmin.auth.schemas import UserSimpleOut
from .case_category import CaseCategorySimpleOut

# 基础案件信息模型定义
class LegalCase(BaseModel):
    category_id: int | None = None
    create_user_id: int | None = None

    title: str | None = None
    content: str | None = None
    view_number: int | None = None
    is_active: bool | None = None


class CaseSimpleOut(LegalCase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    update_datetime: DatetimeStr
    create_datetime: DatetimeStr


class CaseListOut(CaseSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    create_user: UserSimpleOut
    category: CaseCategorySimpleOut
