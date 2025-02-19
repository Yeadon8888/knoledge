from openai import OpenAI
import logging
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

class DeepSeekAPI:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.ppinfra.com/v3/openai",
            api_key=os.getenv("DEEPSEEK_API_KEY", "sk_lBPmVmoH57YDiskY3e2teS-1-Zf-JFlysM7Lh2W6ZSc")
        )
        self.model = "deepseek/deepseek-r1/community"
        self.system_content = """你是一个专业的知识管理助手，你会：
1. 帮助用户管理和组织他们的知识
2. 回答用户关于知识管理的问题
3. 提供知识整理和归类的建议
4. 用简洁清晰的方式表达
5. 始终保持专业和友好的态度

在回答问题时，你会：
1. 先理解用户的问题
2. 提供准确和有价值的信息
3. 适当引用可靠的来源
4. 使用结构化的方式组织回答
5. 在必要时提供进一步的建议

请用中文回答所有问题。"""

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        stream: bool = True,
        max_tokens: int = 10240,
        temperature: float = 0.7,
        top_p: float = 1,
        min_p: float = 0,
        top_k: int = 50,
        presence_penalty: float = 0,
        frequency_penalty: float = 0,
        repetition_penalty: float = 1,
    ) -> Any:
        """
        调用DeepSeek API进行对话
        """
        try:
            # 确保第一条消息是系统提示
            if not messages or messages[0].get("role") != "system":
                messages.insert(0, {
                    "role": "system",
                    "content": self.system_content
                })

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=stream,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                response_format={"type": "text"},
                extra_body={
                    "top_k": top_k,
                    "repetition_penalty": repetition_penalty,
                    "min_p": min_p
                }
            )
            
            if stream:
                return response
            else:
                return response.choices[0].message.content

        except Exception as e:
            logger.error(f"DeepSeek API调用失败: {str(e)}")
            raise

    def get_knowledge_response(self, message: str) -> str:
        """
        获取知识管理相关的回答
        """
        try:
            messages = [
                {
                    "role": "user",
                    "content": message
                }
            ]
            
            response = self.chat_completion(
                messages=messages,
                stream=False,
                temperature=0.7  # 适当的温度以平衡创造性和准确性
            )
            
            return response

        except Exception as e:
            logger.error(f"获取知识回答失败: {str(e)}")
            return f"抱歉，我暂时无法回答您的问题。错误信息：{str(e)}" 