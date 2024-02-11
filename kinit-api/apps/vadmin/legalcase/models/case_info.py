#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# JG_EDIT

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text, Date, Boolean
from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel


from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.db_base import BaseModel

class VadminLegalCase(BaseModel):
    __tablename__ = "legal_cases"
    __table_args__ = ({'comment': '法律案件信息表'})

    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="案件名称")
    icon: Mapped[str] = mapped_column(String(255), nullable=False, comment="图标链接")
    message: Mapped[str] = mapped_column(Text, nullable=False, comment="案件描述")
    personal: Mapped[str] = mapped_column(String(255), nullable=False, comment="个人信息标识")
    link: Mapped[str] = mapped_column(String(255), nullable=False, comment="相关链接")
    time: Mapped[DateTime] = mapped_column(DateTime, nullable=False, comment="时间戳")

    # 假设创建人信息与VadminUser模型有外键关联，如示例所示
    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped['VadminUser'] = relationship(foreign_keys=create_user_id)


class VadminCaseCategory(BaseModel):
    __tablename__ = "vadmin_suetactix_case_cate"
    __table_args__ = {'comment': '案件分类表'}

    cate_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="分类ID")
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True, comment="分类名称")
    description: Mapped[str] = mapped_column(Text, comment="分类描述")

    # 关系定义：假设一个分类可以关联多个案件
    cases: Mapped[list["VadminCaseInfo"]] = relationship( back_populates="category")

class CasePrecedent(BaseModel):
    __tablename__ = "vadmin_suetactix_case_precedent"
    __table_args__ = {'comment': '案例先例表'}

    precedent_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="先例ID")
    case_id: Mapped[int] = mapped_column(Integer, ForeignKey("suetactix_case_info.case_id"), comment="关联案件ID")
    description: Mapped[str] = mapped_column(Text, comment="先例描述")
    legal_basis: Mapped[str] = mapped_column(Text, comment="法律依据")

    # 关系定义：与案件信息表的关系
    case: Mapped[VadminCaseCategory] = relationship(back_populates="precedents")

class VadminCaseInfo(BaseModel):
    __tablename__ = "vadmin_suetactix_case_info"
    __table_args__ = {'comment': '案件信息表'}  # 表级别的注释

    # 定义字段
    case_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="案件ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True, comment="案件标题")
    description: Mapped[str] = mapped_column(Text, comment="案件描述")
    status: Mapped[str] = mapped_column(String(50), nullable=False, comment="案件状态")
    lawyer_id: Mapped[int] = mapped_column(Integer, ForeignKey("vadmin_suetactix_lawyer.lawyer_id"), comment="负责律师ID")
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("vadmin_suetactix_client_table.client_id"), comment="客户ID")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否可见")

    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_suetactix_case_cate.id", ondelete='CASCADE'),
        comment="类别"
    )
    category: Mapped[list[VadminCaseCategory]] = relationship(foreign_keys=category_id, back_populates='issues')

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)


    # 设置关系
    lawyer: Mapped[VadminLawyer] = relationship(back_populates="cases")
    client: Mapped[VadminClient] = relationship(back_populates="cases")
    cases: Mapped[list[VadminCaseCategory]] = relationship(back_populates='category')


class EvidenceChain(BaseModel):
    __tablename__ = "vadmin_suetactix_evidencechain"
    __table_args__ = {'comment': '证据链表'}

    evidence_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="证据ID")
    case_id: Mapped[int] = mapped_column(Integer, ForeignKey("suetactix_case_info.case_id"), comment="关联案件ID")
    description: Mapped[str] = mapped_column(Text, comment="证据描述")
    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="证据类型")
    submission_date: Mapped[str] = mapped_column(String(50), comment="提交日期")

    # 关系定义：与案件信息表的关系
    case: Mapped[VadminCaseInfo] = relationship( back_populates="evidences")
