import logging
import json
from openai import OpenAI

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """你是一个专业的文本分析助手。请从给定文本中提取关键信息，要求：

1. 分析文本内容，识别出所有关键信息类别（例如：学校名称、创建时间、校训等）
2. 提取每个类别对应的具体信息
3. 返回JSON格式，其中：
   - key为信息类别（例如："学校名称", "创建时间", "校训"等）
   - value为对应的信息内容，必须是数组格式
4. 如果某个类别有多个值，将所有值都放入数组
5. 确保返回的是合法的JSON格式，不要添加任何额外说明

示例格式：
{
    "学校名称": ["xxx"],
    "创建时间": ["xxx"],
    "校训": ["xxx"],
    ... （根据实际文本内容提取的其他类别）
}"""

class MoonshotAPI:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
        logger.info("MoonshotAPI initialized")

    def extract_knowledge(self, content: str) -> dict:
        """从文本中提取结构化知识"""
        try:
            # 构建提示词
            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"请分析以下文本并提取所有关键信息：\n\n{content}"
                }
            ]

            # 调用API
            logger.info("Making API call to Moonshot...")
            try:
                response = self.client.chat.completions.create(
                    model="moonshot-v1-8k",
                    messages=messages,
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )
                logger.info("API call successful")
                
                # 获取响应文本
                response_text = response.choices[0].message.content
                logger.debug(f"Raw API Response: {response_text}")

                # 尝试解析JSON
                try:
                    knowledge = json.loads(response_text)
                    logger.info("Successfully parsed JSON response")
                    
                    # 确保所有值都是数组格式
                    for key in knowledge:
                        if not isinstance(knowledge[key], list):
                            knowledge[key] = [knowledge[key]] if knowledge[key] else []
                    
                    return knowledge
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON: {str(e)}")
                    logger.error(f"Invalid JSON response: {response_text}")
                    raise ValueError(f"Invalid JSON response from API: {str(e)}")
                    
            except Exception as e:
                logger.error(f"API call failed: {str(e)}")
                raise ValueError(f"API call failed: {str(e)}")

        except Exception as e:
            logger.error(f"Error in extract_knowledge: {str(e)}")
            raise
