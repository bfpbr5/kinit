from pydantic import BaseModel, Field
from typing import Optional, List,  Union, Optional, Dict

class CaseInput(BaseModel):
    case_id: int = Field(..., ge=1, le=99999999999, description="案卷唯一编号，1-11位整数", example=10010)  
    case_text: str = Field(..., min_length=1, max_length=5000, description="案情描述，5000字以内", example="张三盗窃3000元。") 

class CaseAnalysisInput(BaseModel):
    case_id: int = Field(..., ge=1, le=99999999999, description="案卷唯一编号", example=10010)
    case_text: str = Field(..., min_length=1, max_length=5000, description="案情描述", example="张三盗窃3000元。")
    similar_case_analysis: List[str] = Field(..., min_items=1, max_items=5, description="多个类似案例的分析", example=["南部县人民法院 (2018)川1321刑初132号\n\n本院认为，被告人赖某某以非法占有为目的，盗窃他人财物价值1446元，其行为已构成盗窃罪，依法应予处罚。公诉机关指控被告人赖某某犯盗窃罪的事实清楚，证据确实、充分，罪名成立，本院予以支持。被告人赖某某系又聋又哑的人，可以从轻处罚。被告人赖某某到案后，如实供述自己的罪行，属坦白情节，可以从轻处罚。被告人赖某某积极配合公安机关追缴赃物，给被害人造成的损失较小，可以酌情从轻处罚。被告人赖某某有盗窃犯罪前科，其犯罪时间间隔较短，可以酌定从重处罚。", "本院认为2", "本院认为3"])

class VerificationInput(BaseModel):
    case_id: int = Field(..., ge=1, le=99999999999, description="案卷唯一编号，1-11位整数", example=10010)  
    case_text: str = Field(..., min_length=1, max_length=5000, description="案情描述，5000字以内", example="张三盗窃3000元。") 
    analysis: str = Field(..., min_length=1, description="待验证的案例分析", example="分析内容...")


class CaseChangeInput(BaseModel):
    case_id: int = Field(..., ge=1, le=99999999999, description="案卷唯一编号", example=10010)
    case_text: str = Field(..., min_length=1, max_length=5000, description="案情描述", example="张三盗窃3000元。")
    original_analysis: str = Field(..., min_length=1, description="原始案例分析", example="原始分析内容...")
    additional_information: str = Field(..., min_length=1, description="新增加的案件信息", example="张三抢劫3000元")

class ExplanationInput(BaseModel):
    case_id: int = Field(..., ge=1, le=99999999999, description="案卷唯一编号，1-11位整数", example=10010)
    case_text: str = Field(..., min_length=1, max_length=5000, description="案情描述，5000字以内", example="张三盗窃3000元。")
    analysis: str = Field(..., min_length=1, description="需要进一步解释的案例分析", example="分析内容...")

class KeywordsInput(BaseModel):
    case_id: Optional[int] = Field(None, ge=1, le=99999999999, description="案卷唯一编号", example=10010)
    case_text: str = Field(..., min_length=1, max_length=5000, description="案情描述", example="张三盗窃3000元。")
    case_analysis: Optional[str] = Field(None, min_length=1, description="案例分析", example="分析内容...")

class EvidenceInput(BaseModel):
    evidence_id: int = Field(..., ge=1, le=99999999999, description="证据唯一编号，1-11位整数", example=10010) 
    analysis_results: Union[dict, str] = Field(...,min_length=1, max_length=3000 ,description="案例分析结果，3000字以内", example={"案件时间线":"2000年1月1日，张三向李四借款3000元", "待澄清问题":"test questions"})


class EvidenceExplanationInput(BaseModel):
    case_id: int = Field(..., ge=1, le=99999999999, description="案卷唯一编号", example=10010)
    case_text: str = Field(..., min_length=1, max_length=5000, description="案情描述", example="张三盗窃3000元。")
    evidence: str = Field(..., min_length=1, description="需要解释必要性的证据", example="监控录像。")


class OcrInput(BaseModel):
    raw_text: str = Field(..., min_length=1, max_length=5000, description="OCR生成的原始文本，5000字以内", example="""8:44
交易记录
99
自v
李四(******************)
2017年04月
支出￥10,000.00
3
李四****借出
-￥10000.00
储蓄卡****""")  


class CheckEvidenceInput(BaseModel):
    needed_evidence: str = Field(..., min_length=1, max_length=2000, description="所需证据的详细信息，2000字以内", example="张三的银行转账记录或现金取款记录，以证明借款的支付事实。")    
    organized_ocr: str = Field(..., min_length=1, max_length=2000, description="整理后的 OCR 文本，2000字以内", example="张三的银行转账记录如下：- 2017年04月，李四向张三(*******)转账支出￥10,000.00。")    


class ChatInput(BaseModel):
    user_message: str = Field(..., min_length=1, max_length=500, description="用户的消息，500字以内", example="解释一下这个案子的案由")    # 1-5000位字符串
    case_text: Optional[str] = Field(None, min_length=1, max_length=2000, description="案件文本，2000字以内")    # 1-5000位字符串
    history: Optional[List[Dict[str, str]]] = Field(None, description="历史记录，以 OpenAI 官方 messages 列表格式输入", example=[{'role':'user', 'content':'user messages'}, {'role':'assistant', 'content':'ai responses'}])


class AnalysisChatInput(BaseModel):
    case_id: int = Field(..., ge=1, le=99999999999, description="案卷唯一编号", example=10010)
    case_text: str = Field(..., min_length=1, max_length=5000, description="案情描述", example="张三盗窃3000元。")
    analysis: str = Field(..., min_length=1, description="案例分析", example="分析内容...")
    chat_text: str = Field(..., min_length=1, description="用户的聊天文本", example="请问这个分析的关键点是什么？")
    history: List[Dict[str, str]] = Field(default=None, description="对话历史，可选。格式为交替的'assistant'和'user'消息列表，以'user'消息开始，'assistant'信息结束", example=[{"role":"user", "content":"user messages"}, {"role":"assistant", "content":"assistant messages"}])


class GeneralChatInput(BaseModel):
    user_message: str = Field(..., min_length=1, max_length=500, description="用户的消息，500字以内", example="刚刚我们聊了什么")    # 1-5000位字符串
    history: Optional[List[Dict[str, str]]] = Field(None, description="历史记录，以 OpenAI 官方 messages 列表格式输入", example=[{'role':'user', 'content':'user messages'}, {'role':'assistant', 'content':'ai responses'}])


class EmbeddingInput(BaseModel):
    input_text: str = Field(..., min_length=1, description="输入文本以生成嵌入向量", example="示例文本。")
    
class SearchQueryInput(BaseModel):
    search_query: str = Field(..., min_length=1, description="生成专用于待检索 query 的嵌入向量", example="示例query。")