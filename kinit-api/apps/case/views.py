#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/10/19 15:41
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 简要说明

from fastapi import APIRouter, Depends, UploadFile, Body, HTTPException
from apps.vadmin.auth.utils.current import AllUserAuth
from utils.file.file_manage import FileManage
from utils.response import SuccessResponse
from apps.vadmin.auth.utils.validation.auth import Auth
from . import schemas, crud, models
from .services.full_ai_unit_lc import CaseAnalyzer, EvidenceAnalyzer

app = APIRouter()

CAzer = CaseAnalyzer()
EAzer = EvidenceAnalyzer()

###########################################################
#    案情分析
###########################################################
@app.post("/create", summary="创建案件")
async def create_case(data: schemas.Case, auth: Auth = Depends(AllUserAuth())):
    new_case = await crud.CaseDal(auth.db).create_data(data=data)
    return SuccessResponse(new_case)


@app.post("/analysis/{data_id}", summary="案情分析")
async def case_analysis(data_id: int, desc: str = Body(...), auth: Auth = Depends(AllUserAuth())):
    res_data = await CAzer.analyze_async(case_text=desc)
    res_data["desc"] = desc
    
    if res_data:
        await crud.CaseDal(auth.db).put_data(data_id=data_id, data=res_data)
        return SuccessResponse(res_data)
    else:
        raise HTTPException(status_code=400, detail="案情分析请求参数错误")
    


@app.post("/analysis/file/upload/to/local/{data_id}", summary="上传案情分析文件到本地")
async def upload_analysis_image_to_local(data_id: int, file: UploadFile, auth: Auth = Depends(AllUserAuth())):
    manage = FileManage(file, "case")
    path = await manage.save_image_local(["image/png", "image/jpeg", "application/pdf"])
    await crud.CaseDal(auth.db).put_data(data_id=data_id, data={"case_file": path.get("remote_path")})
    return SuccessResponse(path)


@app.post("/explain/analysis/{data_id}", summary="案情分析")
async def explain_analysis(data_id: int, data: str = Body(...), auth: Auth = Depends(AllUserAuth())):
    case_info = await crud.CaseDal(auth.db).get_data(id=data_id)
    res_data = CAzer.explain_analysis(case_text=case_info.desc, analysis=data)
    if res_data:
        # data = "由于提供的案件信息极为简略，且初始分析内容为空，以下分析将基于中国民法和刑法的相关规定，对张三的盗窃行为进行深入分析，并尝试提出可能的法律后果。\n\n### 1. 盗窃行为的性质和法律责任\n\n根据中国的刑法规定，盗窃是指非法占有的目的，秘密窃取他人财物的行为。张三盗窃的金额为3000元，这一行为明确构成了盗窃罪。在中国，盗窃罪的法律责任是根据盗窃金额的多少和行为人是否有其他不良记录等因素来确定的。\n\n### 2. 法律后果\n\n- **量刑标准**：根据中国刑法的相关规定，盗窃金额数额较大（一般指数千至数万元人民币），并且没有其他加重情节的，可能被判处三年以下有期徒刑、拘役或者管制，并处或者单处罚金。由于张三盗窃的金额为3000元，这一金额属于较小数额，因此，张三可能面临的刑事责任相对较轻。\n\n- **情节加重因素**：如果张三此前有盗窃前科或者是在特殊时期（如自然灾害、事故灾难期间）进行盗窃，或盗窃公共财物、国有公司、企业、事业单位、人民团体的财物，那么其所承担的法律责任可能会加重。\n\n- **民事责任**：除刑事责任外，张三还可能承担民事赔偿责任。根据中国民法的规定，侵害他人财产权利的，应当承担赔偿损失的责任。因此，张三有可能需要向被盗窃方赔偿3000元及可能的间接损失。\n\n### 3. 法律程序\n\n张三的案件将经过立案、侦查、审查起诉和审判几个阶段。在此过程中，张三有权获得法律援助，包括委托辩护律师参与案件的各个环节，保护自己的合法权益。\n\n### 4. 分析扩展\n\n- **个案与法律规定的关系**：分析张三的案件，可以看出个案分析离不开具体法律规定的支撑。对于盗窃罪的认定及其量刑，需要基于刑法的明文规定进行。\n\n- **法律适用的灵活性**：尽管法律对于盗窃行为有明确的规定，但在实际操作中，法官在判决时往往会考虑案件的具体情况，例如被告人的悔罪表现、是否有赔偿被害人的意愿和能力等因素，从而作出更为公正合理的判决。\n\n- **预防和教育的重要性**：从根本上减少此类犯罪的发生，不仅需要法律的严格制裁，还需要社会各界特别是家庭、学校等基本社会单位加强法治教育和道德教育，提高公民的法律意识和道德观念。\n\n综上所述，张三的盗窃行为不仅触犯了刑法，还可能需要承担相应的民事责任。此案件亦反映出法律适用的灵活性以及预防和教育的重要性。"
        return SuccessResponse(res_data)
    else:
        raise HTTPException(status_code=400, detail="案情分析请求参数错误")
    


@app.post("/verify/analysis/{data_id}", summary="案情验证")
async def verify_analysis(data_id: int, data: str = Body(...), auth: Auth = Depends(AllUserAuth())):
    case_info = await crud.CaseDal(auth.db).get_data(id=data_id)

    res_data = CAzer.verify_analysis(case_text=case_info.desc, analysis=data)
    # data = "考虑到案件详情仅提供了非常简短的信息，即“张三盗窃3000元”，而没有给出具体的案件分析内容，我将基于该案件的基本情况进行一般性的评估分析。\n\n首先，案件涉及的主要法律问题是盗窃行为。盗窃作为一种侵犯公民财产所有权的行为，在中国民法和刑法中都有明确的规定。根据相关法律，盗窃行为的认定需要满足特定条件，包括但不限于非法占有的目的、秘密窃取他人财物等特征。\n\n案件详情虽简，但指出张三盗窃了3000元，这意味着张三的行为已构成盗窃。在进行法律分析时，应当考虑以下几个方面：\n\n1. **行为人的主观意图和行为方式**：张三是否有非法占有的目的，其盗窃的行为是否是秘密进行的。\n2. **被盗财物的价值**：被盗财物的价值对于判决结果有重要影响。虽然3000元可能不会触及较高刑事责任的起点，但仍然是刑事责任的可能范围内。\n3. **可能的情节和从轻、减轻情节**：比如张三是否属于初犯、是否有自首情节、是否有返还财物等行为，这些都会影响最终的法律后果。\n\n由于分析内容未给出，我无法直接对其准确性和合理性进行评价。但根据案件的基本情况，任何有效的分析都应当围绕上述几个方面进行。一个合理的法律分析应该不仅指出行为的法律性质，还应当对可能的刑事责任范围、相关的法律适用以及判决建议进行综合考虑。\n\n总的来说，在没有具体分析内容的情况下，评估张三的案件应依据其行为特征、法律规定及可能的情节等因素进行全面分析。一个准确和合理的分析应当深入探讨这些方面，以便于形成对案件合理的法律认定和判断。"
    return SuccessResponse(res_data)

# @app.post("/chain_list/{data_id}", summary="证据链列表")
# async def chain_list_by_caseid(data_id: int, data: str = Body(...),  auth: Auth = Depends(AllUserAuth())):
#     res_data = await crud.CaseDal(auth.db).get_data(id=data_id)
#     return SuccessResponse(res_data)

@app.post("/chain/of/evidence/generate/{data_id}", summary="证据链生成")
async def chain_of_evidence_generate(data_id: int, data: str = Body(...),  auth: Auth = Depends(AllUserAuth())):

    case_info = await crud.CaseDal(auth.db).get_data(id=data_id)
    print("="*30, case_info)
    res_datas = EAzer.analyze( case_info.desc)
    print(res_datas)
    insert_data = []
    for res_data in res_datas:
        if res_data:
            insert_data.append({
                "case_id": res_data['evidence_id'],
                "content": res_data['evidence'],
                "upload_status": False
            })
    print(res_data)
    # res_data = [
    #     {
    #         "case_id": data_id,
    #         "content": "张三与李四之间借款合同或书面借条。",
    #         "upload_status": False
    #     },
    #     {
    #         "case_id": data_id,
    #         "content": "张三的银行账户流水，证明其在2000年1月1日前后有3000元的支出。",
    #         "upload_status": False
    #     },
    #     {
    #         "case_id": data_id,
    #         "content": "李四的银行账户流水，证明其在2000年1月1日前后收到3000元。",
    #         "upload_status": False
    #     },
    #     {
    #         "case_id": data_id,
    #         "content": "双方的通信记录，证明借款事宜的讨论。",
    #         "upload_status": False
    #     }
    # ]
    await crud.ChainOfEvidenceDal(auth.db).create_datas(datas=insert_data)
    datas = await crud.ChainOfEvidenceDal(auth.db).get_datas(limit=0, v_schema=schemas.ChainOfEvidenceSimpleOut, case_id=data_id)
    return SuccessResponse(datas)


@app.post("/chain/of/evidence/file/upload/to/local/{data_id}", summary="上传证据链文件到本地")
async def upload_chain_of_evidence_file_to_local(file: UploadFile, data_id: int, auth: Auth = Depends(AllUserAuth())):
    manage = FileManage(file, "case")
    path = await manage.save_image_local(["image/png", "image/jpeg", "application/pdf"])
    path["data_id"] = data_id
    await crud.ChainOfEvidenceDal(auth.db).put_data(data_id, {"upload_status": True, "file_url": path.get("remote_path")})
    return SuccessResponse(path)

