# encoding: utf-8  #
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pprint import pprint
from starlette.requests import Request
from pydantic import BaseModel, Field
from typing import Optional
import asyncio

from typing import Union, Optional, List, Dict
# from api.services.full_ai_unit import CaseAnalyzer, EvidenceAnalyzer, SimilarCaseFinder, LitigationStrategist, ChatBot, ChatBotGeneral, EmbeddingCreator
from api.services.full_ai_unit_lc import CaseAnalyzer, EvidenceAnalyzer
# 重启： systemctl restart fastapi.service
# 查看调试：systemctl status fastapi.service

router_analysis = APIRouter(
    prefix="/lawyer",
    tags=["Analysis"],
    
)
router_evidence = APIRouter(
    prefix="/lawyer",
    tags=["Evidence"],
    
)
router_debug = APIRouter(
    prefix="/lawyer",
    tags=["Debug"],
    
)



class CaseInput(BaseModel):
    case_id: int = Field(..., ge=1, le=99999999999, description="案卷唯一编号，1-11位整数", example=10010)  
    case_text: str = Field(..., min_length=1, max_length=5000, description="案情描述，5000字以内", example="张三盗窃3000元。") 

@router_analysis.post("/analyze_case/")
async def analyze_case(case_input: CaseInput):
    """### 案例分析模块

    1. 输⼊/输出规格  
    -    输⼊: ⽤⾃然语⾔描述的案例。  
    -    输出: 案例背景、起诉案由、诉讼请求、需澄清信息、所需的证据。  
    """
    case_text = case_input.case_text
    case_id = case_input.case_id
    if not case_text:
        raise HTTPException(status_code=400, detail="Case text not provided")
    
    analyzer = CaseAnalyzer()
    # full_analysis = analyzer.analyze(case_text)
    full_analysis = await analyzer.analyze_async(case_text)
    # full_analysis = analyzer.cause_analysis_test(case_text)
    return full_analysis

class CaseAnalysisInput(BaseModel):
    case_id: int = Field(..., ge=1, le=99999999999, description="案卷唯一编号", example=10010)
    case_text: str = Field(..., min_length=1, max_length=5000, description="案情描述", example="张三盗窃3000元。")
    similar_case_analysis: List[str] = Field(..., min_items=1, max_items=5, description="多个类似案例的分析", example=["南部县人民法院 (2018)川1321刑初132号\n\n本院认为，被告人赖某某以非法占有为目的，盗窃他人财物价值1446元，其行为已构成盗窃罪，依法应予处罚。公诉机关指控被告人赖某某犯盗窃罪的事实清楚，证据确实、充分，罪名成立，本院予以支持。被告人赖某某系又聋又哑的人，可以从轻处罚。被告人赖某某到案后，如实供述自己的罪行，属坦白情节，可以从轻处罚。被告人赖某某积极配合公安机关追缴赃物，给被害人造成的损失较小，可以酌情从轻处罚。被告人赖某某有盗窃犯罪前科，其犯罪时间间隔较短，可以酌定从重处罚。", "本院认为2", "本院认为3"])


class VerificationInput(BaseModel):
    case_id: int = Field(..., ge=1, le=99999999999, description="案卷唯一编号，1-11位整数", example=10010)  
    case_text: str = Field(..., min_length=1, max_length=5000, description="案情描述，5000字以内", example="张三盗窃3000元。") 
    analysis: str = Field(..., min_length=1, description="待验证的案例分析", example="分析内容...")


@router_analysis.post("/verify_analysis/")
async def verify_analysis(verification_input: VerificationInput):
    """### 案例分析验证模块

    1. 输⼊/输出规格  
    -    输⼊: 案件描述及待验证的案例分析。  
    -    输出: 分析的验证结果。  
    """
    case_text = verification_input.case_text
    analysis = verification_input.analysis
    case_id = verification_input.case_id

    if not case_text or not analysis:
        raise HTTPException(status_code=400, detail="Case text or analysis not provided")

    analyzer = CaseAnalyzer()
    verification_result = analyzer.verify_analysis(case_text, analysis)

    return {"case_id": case_id, "verification_result": verification_result}

class ExplanationInput(BaseModel):
    case_id: int = Field(..., ge=1, le=99999999999, description="案卷唯一编号，1-11位整数", example=10010)
    case_text: str = Field(..., min_length=1, max_length=5000, description="案情描述，5000字以内", example="张三盗窃3000元。")
    analysis: str = Field(..., min_length=1, description="需要进一步解释的案例分析", example="分析内容...")

@router_analysis.post("/explain_analysis/")
async def explain_analysis_route(explanation_input: ExplanationInput):
    """### 案例分析解释模块

    1. 输⼊/输出规格  
    -    输⼊: 案件描述及需要进一步解释的案例分析。  
    -    输出: 分析的详细解释。  
    """
    case_text = explanation_input.case_text
    analysis = explanation_input.analysis
    case_id = explanation_input.case_id

    if not case_text or not analysis:
        raise HTTPException(status_code=400, detail="Case text or analysis not provided")

    analyzer = CaseAnalyzer()
    explanation = analyzer.explain_analysis(case_text, analysis)

    return {"case_id": case_id, "explanation": explanation}


class EvidenceInput(BaseModel):
    evidence_id: int = Field(..., ge=1, le=99999999999, description="证据唯一编号，1-11位整数", example=10010) 
    analysis_results: Union[dict, str] = Field(...,min_length=1, max_length=3000 ,description="案例分析结果，3000字以内", example={"案件时间线":"2000年1月1日，张三向李四借款3000元", "待澄清问题":"test questions"})

@router_evidence.post("/analyze_evidence/")
async def analyze_evidence(evidence_input: EvidenceInput):
    """### 证据分析模块  

    1. 功能要求  
    -    分析案件，推断和列出所需的证据。  
    -    使用正则表达式按项目编号分割文本。  

    2. 输⼊/输出规格  
    -    输⼊: 案件分析结果，以键值对表示各模块（如案由）及其信息。  
    -    输出: 与案例关联后的分析证据。  
    
    """
    analysis_results = evidence_input.analysis_results
    evidence_id = evidence_input.evidence_id
    if not analysis_results:
        raise HTTPException(status_code=400, detail="Analysis results not provided")
    
    analyzer = EvidenceAnalyzer()
    full_analysis = analyzer.analyze(analysis_results)
    result_parts = analyzer.split_analysis(full_analysis)
    
    return {
        "evidence_id": evidence_id,
        "evidence": result_parts
    }

class EvidenceExplanationInput(BaseModel):
    case_id: int = Field(..., ge=1, le=99999999999, description="案卷唯一编号", example=10010)
    case_text: str = Field(..., min_length=1, max_length=5000, description="案情描述", example="张三盗窃3000元。")
    evidence: str = Field(..., min_length=1, description="需要解释必要性的证据", example="监控录像。")


@router_evidence.post("/explain_evidence_need/")
async def explain_evidence_need_route(evidence_input: EvidenceExplanationInput):
    """### 证据必要性解释模块

    1. 输⼊/输出规格  
    -    输⼊: 案件描述及需解释必要性的证据。  
    -    输出: 证据必要性的详细解释。  
    """
    case_text = evidence_input.case_text
    evidence = evidence_input.evidence
    case_id = evidence_input.case_id

    if not case_text or not evidence:
        raise HTTPException(status_code=400, detail="Case text or evidence not provided")

    analyzer = EvidenceAnalyzer()
    explanation = analyzer.explain_evidence_need(case_text, evidence)

    return {"case_id": case_id, "evidence_explanation": explanation}



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

@router_evidence.post("/organize_ocr/")
async def organize_ocr(ocr_input: OcrInput):
    """### OCR整理模块  

    1. 功能要求  
    -    整理 OCR 生成的原始文本。  

    2. 输⼊/输出规格  
    -    输⼊: OCR生成的原始文本。  
    -    输出: 整理后的文本。  
    
    """
    raw_text = ocr_input.raw_text
    if not raw_text:
        raise HTTPException(status_code=400, detail="Raw text not provided")
    
    analyzer = EvidenceAnalyzer()
    organized_text = analyzer.organize_ocr(raw_text)
    
    return {
        "organized_text": organized_text
    }

class CheckEvidenceInput(BaseModel):
    needed_evidence: str = Field(..., min_length=1, max_length=2000, description="所需证据的详细信息，2000字以内", example="张三的银行转账记录或现金取款记录，以证明借款的支付事实。")    
    organized_ocr: str = Field(..., min_length=1, max_length=2000, description="整理后的 OCR 文本，2000字以内", example="张三的银行转账记录如下：- 2017年04月，李四向张三(*******)转账支出￥10,000.00。")    

@router_evidence.post("/check_evidence_valid/")
async def check_evidence_valid(check_evidence_input: CheckEvidenceInput):
    """
    向 EvidenceAnalyzer 的 check_evidence_valid 方法输入一条证据文本和一条待比对文本，输出比对结果
    """
    needed_evidence = check_evidence_input.needed_evidence

    organized_ocr = check_evidence_input.organized_ocr
    analyzer = EvidenceAnalyzer()
    evidence_analysis = analyzer.check_evidence_valid(needed_evidence, organized_ocr)
    return {"evidence_analysis": evidence_analysis}


# 增加查看日志
import os
import glob
from datetime import datetime, timedelta


class LogInput(BaseModel):
    last_minutes: int = Field(..., ge=1, le=600, description="查看最近多少分钟以内的日志文件", example=60)  
    token: str = Field(..., min_length=11, max_length=11, description="16位访问密码", example="xxxxxxxxxxxxxxxx") 

@router_debug.post("/logs/")
async def read_logs(loginput: LogInput):
    if loginput.token != '13903563281':
        raise HTTPException(status_code=401, detail="Incorrect token")
    now = datetime.now()
    last_time_ago = now - timedelta(minutes=loginput.last_minutes)  # 获取last_minutes分钟前的时间

    # 获取当前脚本的路径
    current_path = os.path.dirname(os.path.realpath(__file__))
    log_dir = os.path.join(current_path, '..', '..', 'logs') # 日志文件的路径

    # 获取所有日志文件
    log_files = glob.glob(os.path.join(log_dir, '*.log*'))

    # 找出最近60分钟的日志文件
    recent_files = []
    for file in log_files:
        if file[-4:] == '.log':
            recent_files.append(file)
            continue
        # 假设文件名的格式为 'log_YYYYMMDD_HHMM.log'
        timestamp = os.path.getmtime(file)
        last_modified_time = datetime.fromtimestamp(timestamp)
        if last_modified_time >= last_time_ago:
            recent_files.append(file)
    # 如果有多个日志文件，需要先合并多个文件内容为一个长字符串
    combined_content = ""
    for fname in recent_files:
        with open(fname) as infile:
            combined_content += infile.read() + "\n\n"
    return combined_content


@router_debug.post("/chat_logs/")
async def read_chat_logs(loginput: LogInput):
    if loginput.token != '13903563281':
        raise HTTPException(status_code=401, detail="Incorrect token")

    # 获取当前脚本的路径
    current_path = os.path.dirname(os.path.realpath(__file__))
    chat_log_file = os.path.join(current_path, '..', '..', 'logs', 'chat_data.log')   # 日志文件的路径
    result = ''
    with open(chat_log_file) as fp:
        result = fp.read()
    if not result:
        result = 'No chat logs'
    return result


class UploadInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000000, description="文件内容，复制粘贴到这里", example="要上传的文件内容,一次性全部复制粘贴到这里") 
    save_path: str = Field(..., min_length=1, max_length=50, description="要保存的文件目录，从api开始", example="./api/services/") 
    save_file_name: str = Field(..., min_length=1, max_length=50, description="要保存的文件名", example="demo.py") 

@router_debug.post("/uploadtext/")
async def upload_text(loginput: LogInput, uploadinput: UploadInput):
    if loginput.token != '13903563281':
        raise HTTPException(status_code=401, detail="Incorrect token")
    try:
        # 确保保存路径存在
        if not os.path.exists(uploadinput.save_path):
            os.makedirs(uploadinput.save_path)

        # 保存文件
        with open(os.path.join(uploadinput.save_path, uploadinput.save_file_name), "w", encoding='utf8') as f:
            f.write(uploadinput.text)

        return {"message": "Text saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File upload failed: {e}")
    

@router_debug.post("/restart/")
async def restart(loginput: LogInput):
    if loginput.token != '13903563281':
        raise HTTPException(status_code=401, detail="Incorrect token")
    try:
        os.system("sudo systemctl restart fastapi.service")
        return {"status": "FastAPI application is restarting."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# @router.post("/zhipu_chat/")
# async def zhipu_chat(chat_input: ChatInput):
#     # user_message = chat_input.user_message
#     messages = [{'role':'user', 'content': chat_input.user_message}]
#     Cca = CallChatAPI()
#     return Cca.call_chat_api(model_name='chatglm_6b', messages=messages)
