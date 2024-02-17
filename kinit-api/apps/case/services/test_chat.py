# coding:utf8
import re
import os
import zhipuai
import openai
import asyncio
import random
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAI
import logging

logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='logs/chat_data.log',
                        filemode='a')

def write_log(messages, text_type='messages'):
    # 使用logging模块来记录日志
    if text_type == 'messages':
        logging.info(messages)
    else:
        logging.debug(messages)
        
class TestChatAPI:
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
