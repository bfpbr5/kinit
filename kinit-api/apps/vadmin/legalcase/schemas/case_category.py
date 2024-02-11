#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
#JG_EDIT

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Optional
from core.data_types import DatetimeStr
from apps.vadmin.auth.schemas import UserSimpleOut


#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr
from apps.vadmin.auth.schemas import UserSimpleOut


class CaseCategory(BaseModel):
    name: str  # 分类名称
    description: Optional[str] = None  # 分类描述，可选字段
    is_active: bool | None = None

    create_user_id: int | None = None


class CaseCategorySimpleOut(CaseCategory):
    model_config = ConfigDict(from_attributes=True)

    id: int
    update_datetime: DatetimeStr
    create_datetime: DatetimeStr


class CaseCategoryListOut(CaseCategorySimpleOut):
    model_config = ConfigDict(from_attributes=True)

    create_user: UserSimpleOut


class CaseCategoryOptionsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    label: str = Field(alias='name')
    value: int = Field(alias='id')

