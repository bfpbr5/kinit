#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/2/15 13:41
# @File           : case.py
# @IDE            : PyCharm
# @desc           : 常见问题

from datetime import date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Integer, ForeignKey, Text, Date


class Case(BaseModel):
    __tablename__ = "case_case"
    __table_args__ = ({'comment': '案件表'})

    name: Mapped[str] = mapped_column(String(255), index=True, comment="案件名称")
    case_datetime: Mapped[date] = mapped_column(Date, comment='案件时间')
    case_file: Mapped[str | None] = mapped_column(String(1000), comment='案情描述文件')
    desc: Mapped[str | None] = mapped_column(Text, comment='案情描述')
    cause: Mapped[str | None] = mapped_column(Text, comment='案由')
    claim: Mapped[str | None] = mapped_column(Text, comment='诉讼请求')
    timeline: Mapped[str | None] = mapped_column(Text, comment='时间线')
    relation: Mapped[str | None] = mapped_column(Text, comment='案情综述')
    questions: Mapped[str | None] = mapped_column(Text, comment='待澄清问题')


class ChainOfEvidence(BaseModel):
    __tablename__ = "case_chain_of_evidence"
    __table_args__ = ({'comment': '案件证据链表'})

    content: Mapped[str | None] = mapped_column(Text, comment='证据内容')
    file_url: Mapped[str | None] = mapped_column(String(1000), comment='证据上传文件')
    upload_status: Mapped[bool] = mapped_column(Boolean, default=False, comment='是否已上传文件')

    case_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("case_case.id", ondelete='RESTRICT'),
        comment="关联案件"
    )
    case: Mapped[Case] = relationship(foreign_keys=case_id)
