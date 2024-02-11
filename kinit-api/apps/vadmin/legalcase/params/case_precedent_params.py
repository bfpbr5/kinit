from typing import Optional, List
from pydantic import BaseModel, Field

# 案例先例查询参数定义
class CasePrecedentQueryParams(BaseModel):
    case_id: Optional[int] = None  # 关联案件ID查询参数，可选
    legal_basis: Optional[str] = None  # 法律依据查询参数，可选

    class Config:
        schema_extra = {
            "example": {
                "case_id": 1,
                "legal_basis": "法律依据示例"
            }
        }

# 案例先例排序参数定义
class CasePrecedentSortParams(BaseModel):
    sort_by: Optional[List[str]] = Field(default=["precedent_id"], description="排序依据的字段列表")
    order_by: Optional[str] = Field(default="asc", description="排序方式，'asc'为升序，'desc'为降序")

    class Config:
        schema_extra = {
            "example": {
                "sort_by": ["case_id"],
                "order_by": "asc"
            }
        }
