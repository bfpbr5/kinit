from typing import Optional, List
from pydantic import BaseModel, Field


from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class UserParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            name: str | None = Query(None, title="用户名称"),
            telephone: str | None = Query(None, title="手机号"),
            email: str | None = Query(None, title="邮箱"),
            is_active: bool | None = Query(None, title="是否可用"),
            is_staff: bool | None = Query(None, title="是否为工作人员"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)
        self.telephone = ("like", telephone)
        self.email = ("like", email)
        self.is_active = is_active
        self.is_staff = is_staff

# 案件信息查询参数定义
class CaseInfoQueryParams(BaseModel):
    title: Optional[str] = None  # 标题查询参数，可选
    status: Optional[str] = None  # 状态查询参数，可选
    lawyer_id: Optional[int] = None  # 负责律师ID查询参数，可选
    client_id: Optional[int] = None  # 客户ID查询参数，可选

    class Config:
        schema_extra = {
            "example": {
                "title": "案件标题示例",
                "status": "处理中",
                "lawyer_id": 1,
                "client_id": 2
            }
        }

# 案件信息排序参数定义
class CaseInfoSortParams(BaseModel):
    sort_by: Optional[List[str]] = Field(default=["case_id"], description="排序依据的字段列表")
    order_by: Optional[str] = Field(default="asc", description="排序方式，'asc'为升序，'desc'为降序")

    class Config:
        schema_extra = {
            "example": {
                "sort_by": ["status", "title"],
                "order_by": "asc"
            }
        }
