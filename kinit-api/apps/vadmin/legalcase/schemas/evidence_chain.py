from pydantic import BaseModel
from typing import Optional

# 证据链的基础模型定义
class EvidenceChainBase(BaseModel):
    case_id: int  # 关联案件的ID
    description: Optional[str] = None  # 证据描述，可选字段
    evidence_type: str  # 证据类型
    submission_date: Optional[str] = None  # 提交日期，可选字段

# 创建证据链时使用的模型，继承自EvidenceChainBase
class EvidenceChainCreate(EvidenceChainBase):
    pass  # 创建证据链时，使用与基础模型相同的字段

# 更新证据链时使用的模型，继承自EvidenceChainBase
class EvidenceChainUpdate(EvidenceChainBase):
    pass  # 更新证据链时，使用与基础模型相同的字段

# 数据库中证据链的模型，包含证据ID，继承自EvidenceChainBase
class EvidenceChainInDBBase(EvidenceChainBase):
    evidence_id: int  # 证据ID

    # 配置Pydantic模型以兼容ORM对象
    class Config:
        orm_mode = True

# 完整的证据链模型，用于API响应
class EvidenceChain(EvidenceChainInDBBase):
    pass  # 包括所有证据链字段

# 数据库内部使用的证据链模型
class EvidenceChainInDB(EvidenceChainInDBBase):
    pass  # 用于与数据库交互的模型
