from typing import Optional, List
from pydantic import BaseModel, Field

# 案件分类查询参数定义
class CaseCategoryQueryParams(BaseModel):
    name: Optional[str] = None  # 分类名称查询参数，可选

    class Config:
        schema_extra = {
            "example": {
                "name": "分类名称示例"
            }
        }

# 案件分类排序参数定义
class CaseCategorySortParams(BaseModel):
    sort_by: Optional[List[str]] = Field(default=["cate_id"], description="排序依据的字段列表")
    order_by: Optional[str] = Field(default="asc", description="排序方式，'asc'为升序，'desc'为降序")

    class Config:
        schema_extra = {
            "example": {
                "sort_by": ["name"],
                "order_by": "asc"
            }
        }
