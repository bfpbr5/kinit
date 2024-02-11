from typing import Optional, List
from pydantic import BaseModel, Field

# 证据链查询参数定义
class EvidenceChainQueryParams(BaseModel):
    case_id: Optional[int] = None  # 关联案件ID查询参数，可选
    evidence_type: Optional[str] = None  # 证据类型查询参数，可选

    class Config:
        schema_extra = {
            "example": {
                "case_id": 1,
                "evidence_type": "证据类型示例"
            }
        }

# 证据链排序参数定义
class EvidenceChainSortParams(BaseModel):
    sort_by: Optional[List[str]] = Field(default=["evidence_id"], description="排序依据的字段列表")
    order_by: Optional[str] = Field(default="asc", description="排序方式，'asc'为升序，'desc'为降序")

    class Config:
        schema_extra = {
            "example": {
                "sort_by": ["evidence_type"],
                "order_by": "asc"
            }
        }
