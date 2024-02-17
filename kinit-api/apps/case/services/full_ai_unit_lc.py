# coding:utf8
from typing import Optional
import re
import os
# import zhipuai
import openai
import asyncio
import random
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import promptlayer
from langchain_community.callbacks import PromptLayerCallbackHandler

import json
from datetime import datetime

# openai.api_base = "https://d1.d100.ren/v1"
os.environ["OPENAI_API_KEY"] = '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'
promptlayer.api_key = "pl_0595bc3db9d174678d4adae0dd6e3cfc"
# openai.api_key = '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'
# zhipuai.api_key = '3e18c16af014d3f53fd684b4a0b345f4.lb4moxfT0EyyC5xI'

def write_log(text, text_type):
    try:
        # with open('/www/wwwroot/hz.d100.ren/logs/chat_data.log', 'a+', encoding='utf8') as f:
        with open('logs/chat_data.log', 'a+', encoding='utf8') as f:
            # 判断是字典
            if isinstance(text, dict):
                text = json.dumps(text, ensure_ascii=False)
            # 判断是列表
            elif isinstance(text, list):
                text = ', '.join(map(str, text))
            # 创建一个日期时间对象  
            now_time = datetime.now()
            now_time_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
            # 加入时间戳
            text = text_type + ': ' + now_time_str + '\n' + text + '\n\n'
            f.write(text)
    except Exception as e:
        print(f"Error writing log: {e}")

class CallChatAPI:
    def call_chat_api(self, model_name: str, messages: list, temperature: float = 0.1, is_async=False):
        write_log(messages, text_type='messages')
        if is_async:
            result = self.chat_zhipuai_async(model_name=model_name, messages=messages, temperature=temperature)
        elif model_name[:3] == 'gpt':
            result = self.chat_openai(model_name=model_name, messages=messages, temperature=temperature)
        elif model_name == 'chatglm_turbo' or  model_name == 'chatglm_pro': 
            result = self.chat_zhipuai(model_name=model_name, messages=messages, temperature=temperature)
        write_log(result, text_type='response')
        return result
        
    def chat_openai(self,  model_name: str, messages: list, temperature:float=0.1):
        
        response = openai.ChatCompletion.create(model_name=model_name, messages=messages, temperature=temperature)
        if 'usage' in response:
            return response['choices'][0]['message']['content']
        else:
             return response
    
    def chat_zhipuai(self,  model_name: str, messages: list, temperature: float = 0.1, top_p: float = 1):
        response = zhipuai.model_api.invoke(
            model=model_name,
            prompt=messages,
            top_p=top_p,
            temperature=temperature
        )
        if response['success']:
            if response['data']['task_status'] == 'SUCCESS':
                choices = response['data']['choices']
                for choice in choices:
                    if choice['role'] == 'assistant':
                        answer = choice['content'].strip('\"').replace('\\n', '\n').strip()
                        # self._add_to_chat_history(question, answer)
                        return answer, response['usage']["total_tokens"]
            else:
                # return "Task failed. Please try again later."
                return response
        else:
            # return "Error occurred. Please check your API key or try again later."
            return response
    
    def chat_zhipuai_async(self, model_name: str, messages: list, temperature: float = 0.1, top_p: float = 1):
        # Initiate an asynchronous call to zhipuai
        zhipuai.api_key = '3e18c16af014d3f53fd684b4a0b345f4.lb4moxfT0EyyC5xI'
        response = zhipuai.model_api.async_invoke(
            model=model_name,
            prompt=messages,
            top_p=top_p,
            temperature=temperature
        )
        print(response)
        return response['data']['task_id'] if response['success'] else None
    
    async def fetch_async_result(self, task_id, max_retries=6, initial_delay=1, max_delay=32):
        delay = initial_delay
        retries = 0

        while retries < max_retries:
            try:
                response = zhipuai.model_api.query_async_invoke_result(task_id)

                # if response['success']:
                if response['data']['task_status'] == 'SUCCESS':
                    print(response)
                    choices = response['data']['choices']
                    for choice in choices:
                        if choice['role'] == 'assistant':
                            return choice['content'].strip('\"').replace('\\n', '\n').strip()

                # Increase delay and retries count
                retries += 1
                await asyncio.sleep(delay)
                delay = min(delay * 2, max_delay) + random.uniform(0, 1)  # Exponential backoff with jitter

            except Exception as e:
                print(f"An error occurred: {e}. Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
                delay = min(delay * 2, max_delay) + random.uniform(0, 1)  # Same backoff logic on exception

        return None
    
    def chat_langchain_openai(self, chain, input):
        result = chain.invoke({"input":input})
        return result


class CaseAnalyzer:
    def __init__(self):
        # Initialize the OpenAI API
        self.chatapi = CallChatAPI()
        # self.model = ChatOpenAI(model="gpt-4-turbo-preview",openai_api_base="https://d1.d100.ren/v1")
        self.model = ChatOpenAI(model="gpt-3.5-turbo",base_url="https://d1.d100.ren/v1",callbacks=[PromptLayerCallbackHandler(pl_tags=["case_analyzer"])],temperature=0.1)
        self.output_parser = StrOutputParser()
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "## Role\n\n{role}\n\n## Task\n\n{task}\n\n## Steps\n\n{step}\n\n## Restriction\n\n{restriction}\n\n## Output Format\n\n{output}"),
            ("user","{input}")
        ])

    async def analyze_async(self, case_text):
        # Send the case details to the API and get the response

        # Define the prompts for each stage of the analysis with the modified structure
        
        timeline_analyzer = self.prompt_template.invoke({
            "role": "A Chinese lawyer well-versed in civil law",
            "task": "Organize the provided case information in chronological order",
            "step": "1. Analyze the provided case information.\n2. Organize the information based on the timeline.\n3. Ensure accuracy and relevance while arranging the information.",
            "restriction": "Do not repeat the case information, start arranging the timeline directly.\nAlways answer in Chinese.",
            "output": "A well-organized timeline of the case information",
            "input": case_text
        })
        relation_analyzer = self.prompt_template.invoke({
            "role": "A Chinese lawyer specializing in civil law, with a thorough understanding of legal principles and judicial practices in the People's Republic of China.",
            "task": "Perform a comprehensive analysis of the legal relationships present in the given case, focusing on the dynamics and implications of these relationships within the context of Chinese civil law.",
            "step": "1. **Case Review**: Thoroughly examine the information provided for the case, paying special attention to the details and nuances that might influence legal relationships.\n2. **Identification of Legal Relationships**: Systematically identify and delineate all the legal relationships entangled in the case. This should include the nature of each relationship, the parties involved, and the legal consequences that may ensue.",
            "restriction": "- **Avoidance of Specific Legal Provisions**: Refrain from directly citing specific laws or statutes, such as stating \"According to Article 264 of the Criminal Law of the People's Republic of China\". The analysis should be conceptual and principle-based rather than reliant on direct legal citations.\n- **Language Specification**: All responses and analyses should be provided exclusively in Chinese, ensuring clarity and precision in the context of Chinese legal terminology and concepts.",
            "output": "Present a well-structured and detailed analysis elucidating the legal relationships identified in the case. The analysis should offer insights into the nature of each relationship, the interplay between different relationships, and their potential legal outcomes, all framed within the scope of Chinese civil law.",
            "input": case_text
        })
        cause_analyzer = self.prompt_template.invoke({
            "role": "中国法律专家，具有深厚的民事与劳动法知识，能够准确地将复杂的法律纠纷案例分类到预定义的类别中。",
            "task": '将提供的案例描述分类到17个预定义的法律纠纷类别中的一个。完整列表如下:categories = ["确认劳动关系纠纷","集体合同纠纷","劳务派遣合同纠纷","非全日制用工纠纷","追索劳动报酬纠纷","经济补偿金纠纷","竞业限制纠纷","养老保险待遇纠纷","工伤保险待遇纠纷","医疗保险待遇纠纷","生育保险待遇纠纷","失业保险待遇纠纷","福利待遇纠纷","聘用合同纠纷","聘任合同纠纷","辞职纠纷","辞退纠纷"]',
            "step": """
                1. **案例描述审查**：仔细阅读提供的案例描述文字，完全理解手头法律问题的背景和具体情况。
                2. **选择三个最合适的类别**：基于案例的输入描述，选择三个最为合适的类别，并描述为什么它们适合。在这一步，考虑案例的细节和与这些类别的匹配度。
                3. **选择最合适的一个类别作为最终答案**：在前两步的基础上，选择一个最合适的类别作为最终分类结果，并给出选择理由。
            """,
            "restriction": """
                - **避免模糊不清**：确保以高度的信心和清晰度进行分类，避免模棱两可的分类。
                - **要求提供理由**：为分类决定提供简要理由，强调导致该分类的案例描述的关键元素。
                - **语言一致性**：以中文进行分析并提供分类理由，确保法律术语的准确性和与中国法律背景的相关性。
            """,
            "output": "案例描述到一个预定义类别的简明分类，附带对决策的简要理由，使用精确的法律术语和分析。",
            "input": case_text
        })
        claim_analyzer = self.prompt_template.invoke({
            "role": "An adept Chinese lawyer specializing in civil law, proficient in case analysis and strategic planning to safeguard client interests.",
            "task": "Critically assess the case to pinpoint litigation claims and formulate robust strategies aimed at optimizing client benefits within the framework of Chinese civil law.",
            "step": "1. **Comprehensive Case Review**: Meticulously scrutinize all case documents and relevant information to fully understand the context and nuances of the case.\n2. **Litigation Claims Identification**: Accurately identify and articulate the litigation claims involved, considering the factual matrix and potential legal implications.\n3. **Strategy Formulation**: Devise and outline strategic approaches tailored to advance the client's interests effectively, focusing on legal precision and tactical foresight.",
            "restriction": "- **Direct Analysis Approach**: Commence your analysis promptly, focusing on the task without unnecessary preludes or personal identifiers.\n- **Avoidance of Specific Legal Citations**: Refrain from directly quoting specific laws or statutes, such as stating \"According to Article 264 of the Criminal Law of the People's Republic of China\". Ensure that the analysis is based on legal understanding and strategic insight rather than mere citation of legal provisions.\n- **Language Requirement**: Maintain all communication and documentation exclusively in Chinese to ensure accuracy in legal terminology and client comprehension.",
            "output": "Deliver a detailed and actionable report that clearly outlines the identified litigation claims and presents well-developed strategies designed to maximize client benefits, adhering to the principles and practices of Chinese civil law.",
            "input": case_text
        })
        questions_analyzer = self.prompt_template.invoke({
            "role": "A proficient Chinese civil law attorney with expertise in meticulous case analysis and information evaluation.",
            "task": "Conduct a detailed assessment of the current information's sufficiency and pinpoint any gaps or ambiguities that require further information or clarification for a comprehensive case analysis.",
            "step": "1. **Information Sufficiency Evaluation**: Scrutinize the provided case information to assess its completeness and relevance in the context of the legal matters at hand.\n2. **Identification of Information Gaps**: Systematically identify and list any missing elements, ambiguities, or areas that necessitate additional information or clarification to facilitate a thorough and accurate case analysis.",
            "restriction": "- **Focused Analysis**: Initiate the assessment without preamble, ensuring a direct and efficient approach to the task.\n- **Avoidance of Direct Legal Citations**: Eschew quoting specific legal provisions directly, such as \"According to Article 264 of the Criminal Law of the People's Republic of China\", maintaining an analysis that is rooted in legal acumen and practical insight.\n- **Language Specificity**: Provide all responses and documentation strictly in Chinese, ensuring precision in legal terminology and alignment with local legal context.",
            "output": "Present a clear and structured report detailing the completeness of the current information and meticulously enumerating any additional data, documents, or clarifications required for an exhaustive and precise analysis of the case.",
            "input": case_text
        })

        prompts = {
            "timeline": timeline_analyzer,
            "relation": relation_analyzer,
            "cause": cause_analyzer,
            "claim": claim_analyzer,
            "questions": questions_analyzer
        }

        async def invoke_async(key, chain, value):
            print(f"Starting analysis for {key}...")  # Progress hint before the operation
            result = await chain.ainvoke(value)
            print(f"Completed analysis for {key}.")  # Progress hint after the operation
            return key, result
        
        # Use asyncio.gather to run all invocations concurrently
        tasks = [invoke_async(key, self.model | self.output_parser, value) for key, value in prompts.items()]
        results = await asyncio.gather(*tasks)
        
        # Construct the result dictionary from the results
        result = dict(results)
        
        return result


    def verify_analysis(self, case_text, analysis):
        # Construct a prompt to verify the analysis
        verification_prompt = self.prompt_template.invoke({
            "role": "一位对中国民法深有研究、在案件审查和逻辑分析方面具有专业精度的律师",
            "task": "对提供的案件材料和相关分析进行细致的审查，并简要评估该分析的准确性和合理性",
            "step": "1. **案件材料细致审阅**: 细致审阅案件详情，确保对每个细节都有深刻理解。\n2. **法律分析审查**: 仔细分析案件的法律分析部分，关注其逻辑结构和论据的合理性。\n3. **综合评估准确性和合理性**: 从案件的关键要素和分析的逻辑严密性出发，综合评估所提供分析的准确性和合理性，确保评估结果具有法律和逻辑上的严谨性。",
            "restriction": "直接开展分析，不需过多强调个人身份背景。\n避免直接引用具体法律条文或法规，例如“根据中华人民共和国刑法第264条”。",
            "output": "对所提供分析的准确性和合理性的清晰、深刻、全面评估",
            "input": "案件详情：```\n" + case_text + "```\n案件分析：```\n" + analysis +"```"
        })


        # Call the chat API for verification
        chain = self.model | self.output_parser
        response = chain.invoke(verification_prompt)

        # Return the response for interpretation
        return response

    def cause_analysis_test(self, case_text):
        # Construct a prompt to verify the analysis
        classification_request = self.prompt_template.invoke({
            "role": "中国法律专家，具有深厚的民事与劳动法知识，能够准确地将复杂的法律纠纷案例分类到预定义的类别中。",
            "task": '将提供的案例描述分类到17个预定义的法律纠纷类别中的一个。完整列表如下:categories = ["确认劳动关系纠纷","集体合同纠纷","劳务派遣合同纠纷","非全日制用工纠纷","追索劳动报酬纠纷","经济补偿金纠纷","竞业限制纠纷","养老保险待遇纠纷","工伤保险待遇纠纷","医疗保险待遇纠纷","生育保险待遇纠纷","失业保险待遇纠纷","福利待遇纠纷","聘用合同纠纷","聘任合同纠纷","辞职纠纷","辞退纠纷"]',
            "step": """
                1. **案例描述审查**：仔细阅读提供的案例描述文字，完全理解手头法律问题的背景和具体情况。
                2. **选择三个最合适的类别**：基于案例的输入描述，选择三个最为合适的类别，并描述为什么它们适合。在这一步，考虑案例的细节和与这些类别的匹配度。
                3. **选择最合适的一个类别作为最终答案**：在前两步的基础上，选择一个最合适的类别作为最终分类结果，并给出选择理由。
            """,
            "restriction": """
                - **避免模糊不清**：确保以高度的信心和清晰度进行分类，避免模棱两可的分类。
                - **要求提供理由**：为分类决定提供简要理由，强调导致该分类的案例描述的关键元素。
                - **语言一致性**：以中文进行分析并提供分类理由，确保法律术语的准确性和与中国法律背景的相关性。
            """,
            "output": "案例描述到一个预定义类别的简明分类，附带对决策的简要理由，使用精确的法律术语和分析。",
            "input": case_text
        })

        # Call the chat API for verification
        chain = self.model | self.output_parser
        response = chain.invoke(classification_request)

        # Return the response for interpretation
        return response

    def explain_analysis(self, case_text, analysis):
        explanation_prompt = self.prompt_template.invoke({
            "role": "深谙民法精髓的中国律师",
            "task": "根据所提供的案件信息，深入解释分析的缘由,如果可能的话,扩展给出的分析",
            "step": "1. **案件信息审阅**: 仔细阅读提供的案件信息，确保对案件的背景、相关事实及细节有透彻的理解。\n2. **初始分析审阅**: 细致研究所提供的初始分析，理解其逻辑结构和论点。\n3. **分析扩展与深化**: 在对案件信息和初始分析的基础上，进行深入分析，提出补充意见或新的视角，确保分析的完整性和深度。",
            "restriction": "确保分析深刻、全面",
            "output": "一个关于所提供案件信息的详细、深刻、全面的分析阐述",
            "input": "案件信息：```\n" + case_text + "```\n初始分析：```\n" + analysis +"```"
        }
)

        chain = self.model | self.output_parser
        response = chain.invoke(explanation_prompt)
        return response


import asyncio

class EvidenceAnalyzer:
    def __init__(self):
        # Initialize the OpenAI API and the prompt template system
        self.chatapi = CallChatAPI()
        self.model = ChatOpenAI(model="gpt-4-turbo-preview",base_url="https://d1.d100.ren/v1",callbacks=[PromptLayerCallbackHandler(pl_tags=["case_analyzer"])],temperature=0.1)  # Assuming model details
        self.output_parser = StrOutputParser()  # Assuming output parsing utility
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "## Role\n\n{role}\n\n## Task\n\n{task}\n\n## Steps\n\n{step}\n\n## Restriction\n\n{restriction}\n\n## Output Format\n\n{output}"),
            ("user", "{input}")
        ])
        self.prompt_template_with_example = ChatPromptTemplate.from_messages([
            ("system", "## Role\n\n{role}\n\n## Task\n\n{task}\n\n## Steps\n\n{step}\n\n## Restriction\n\n{restriction}\n\n## Output Format\n\n{output}\n\n## Example\n\n{example}"),
            ("user", "{input}")
        ])

    def analyze(self, analysis_results):
        '''
        Use the ChatPromptTemplate to dynamically generate and send prompts to the API for evidence analysis.

        Parameters:
            analysis_results (dict or str): The results of case analysis, either as a detailed structure or a simple text.

        Returns:
            str: The response from the API containing the list of required evidence.
        '''
        with open("analyze_debug.txt", "r") as f:
            f.write(str(analysis_results))
        if isinstance(analysis_results, dict):
            case_text = "\n".join(f"{part_name}\n{result_part}" for part_name, result_part in analysis_results.items())
        elif isinstance(analysis_results, str):
            case_text = analysis_results
        else:
            raise ValueError("analysis_results must be either dict or str")

        evidence_prompt = self.prompt_template.invoke({
            "role": "An experienced Chinese lawyer well-versed in civil law",
            "task": "Infer and list what evidence is required for the provided case based on the analysis",
            "step": "1. Review the case analysis and existing situation.\n2. Infer and list the necessary evidence considering the realities of legal litigation.",
            "restriction": "List only evidence that can definitively prove the case's circumstances in court. Avoid legal documents or materials not likely to be presented before litigation. Consider authenticity, legality, and relevance. Do not include more than 10 pieces of evidence. Always response in Chinese.",
            "output": "A list of required evidence without additional explanations, formatted starting with '1.' to clearly separate each part.",
            "input": case_text
        })

        # Assuming the model and output_parser are used to send and parse the API request
        chain = self.model | self.output_parser
        response = chain.invoke(evidence_prompt)

        return response

    def explain_evidence_need(self, case_text, evidence):
        explanation_prompt = self.prompt_template.invoke({
            "role": "A Chinese lawyer proficient in civil law",
            "task": "Explain why the following evidence is necessary based on the case information",
            "step": "Review the case information and evidence provided.\nProvide a brief explanation for the necessity of each piece of evidence.",
            "restriction": "Keep the explanation concise and focused on legality and relevance to the case. Always response in Chinese.",
            "output": "A brief explanation for the necessity of the provided evidence",
            "input": f"Case information:\n```\n{case_text}```\n\nEvidence:\n```\n{evidence}```"
        })

        chain = self.model | self.output_parser
        response = chain.invoke(explanation_prompt)

        return response
    
    def split_analysis(self, response):
        '''
        使用正则表达式按项目编号分割文本。

        参数:
            response (str): OpenAI API 的响应。

        返回:
            list: 分割后的文本列表。
        '''
        # Use a regular expression to split the text by item numbers
        result_parts = re.split(r'\d+\.\s+', response)
        
        # Remove any empty strings resulting from the split
        result_parts = [item.strip() for item in result_parts if item.strip()]
        return result_parts
    
    def evidence_query_prompt(self, needed_evidence):
        '''
        Send detailed information about the required evidence to the API and get a response.
        '''
        evidence_query_prompt = self.prompt_template_with_example.invoke({
            "role": "An experienced Chinese lawyer, skilled in civil law",
            "task": "Identify the key pieces of evidence required from the provided details",
            "step": "1. Review the evidence details provided by the user.\n2. Identify and list the key pieces of evidence necessary for supporting the case.",
            "restriction": "Avoid legal documents or materials not likely to be presented before litigation. Always response in Chinese.",
            "output": "A list of key evidence items, clearly formatted and separated.",
            "example":"“买卖合同的原件或复印件，以证明卢永强与义乌市达勒布苏坦贸易商行之间的买卖关系，以及货款的数额和支付条款等关键信息。”转换为“1. 买卖合同的原件或复印件\n2. 货款的数额\n3. 支付条款”",
            "input": needed_evidence
        })

        chain = self.model | self.output_parser
        response = chain.invoke(evidence_query_prompt)

        self.evid_query = response
        return response

    def organize_ocr(self, raw_text):
        '''
        Organize raw text generated by OCR.
        '''
        organize_ocr_prompt = self.prompt_template.invoke({
            "role": "A diligent assistant tasked with processing fragmented and disorganized text related to a case, generated via OCR",
            "task": "Organize the fragmented, disorganized text into coherent, structured paragraphs",
            "step": "1. Review the OCR-generated text, identifying errors and nonsensical phrases.\n2. Eliminate meaningless fragments and organize the remaining text into coherent paragraphs.",
            "restriction": "Begin your response with 'Original text:'. Only include text that contributes to a clear understanding of the case. Always response in Chinese.",
            "output": "Organized and coherent paragraphs of text, derived from the OCR-generated input",
            "input": raw_text
        })

        chain = self.model | self.output_parser
        organized_ocr = chain.invoke(organize_ocr_prompt)

        return organized_ocr

    def check_evidence_valid(self, needed_evidence, organized_ocr):
        '''
        Check if the collected case materials can substantiate the required evidence.
        '''
        check_evidence_valid_prompt = self.prompt_template.invoke({
            "role": "A professional Chinese lawyer analyzing case materials to substantiate required evidence",
            "task": "Examine the case materials to determine if they support the needed evidence, providing analysis and conclusion",
            "step": "1. Review the detailed evidence requirements provided.\n2. Analyze the organized OCR text to see if it supports the needed evidence.\n3. Provide your analysis process and conclusion.",
            "restriction": "Start your analysis immediately after understanding the task. Respond with 'Okay' to indicate comprehension. Always response in Chinese.",
            "output": "A detailed analysis of whether the case materials support the required evidence, with clear conclusions drawn",
            "input": f"Required evidence details:\n```\n{needed_evidence}```\n\nOrganized OCR text:\n```\n{organized_ocr}```"
        })

        chain = self.model | self.output_parser
        evidence_analysis = chain.invoke(check_evidence_valid_prompt)

        return evidence_analysis

    
    def check_evidence_valid_gpt(self, needed_evidence, organized_ocr):
        '''
        检查收集到的案件材料是否能证实所需的证据。

        参数:
            needed_evidence (str): 所需证据的详细信息。
            organized_ocr (str): 整理后的 OCR 文本。

        返回:
            str: OpenAI API 的响应，包含证据分析的结果。
        '''
        system_prompt = "你是一名专业中国律师,你的任务是检查案件材料能否佐证所需证据,给出分析过程和结论"
        user_prompt = "以下为所需证据:###\n" + needed_evidence + "\n###\n以下为收集到的相关案件材料,其中当事人与信息均与本案件有关:###\n" + organized_ocr + "\n###"
        # Send the case details to the API and get the response
        # model_name = 'gpt-4'
        # model_name = 'chatglm_turbo'
        # response = self.chatapi.call_chat_api(
        from openai import OpenAI
        client = OpenAI(base_url="https://d1.d100.ren/v1")

        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        )
        evidence_analysis = response['choices'][0]['message']['content']
        return evidence_analysis