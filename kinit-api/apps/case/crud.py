#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/02/15 18:43
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models, schemas


class CaseDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(CaseDal, self).__init__()
        self.db = db
        self.model = models.Case
        self.schema = schemas.CaseSimpleOut


class ChainOfEvidenceDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ChainOfEvidenceDal, self).__init__()
        self.db = db
        self.model = models.ChainOfEvidence
        self.schema = schemas.ChainOfEvidenceSimpleOut
