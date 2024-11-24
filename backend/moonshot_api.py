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

MERGE_PROMPT = """你是一个专业的知识融合助手。请合并给定的多个JSON知识内容，要求：

1. 分析所有JSON内容，识别相同和不同的信息类别
2. 对于相同类别的信息：
   - 去除重复内容
   - 保留所有不重复的信息
   - 确保信息的完整性和准确性
3. 对于不同类别的信息：
   - 保留所有类别及其信息
4. 返回合并后的JSON格式，确保：
   - 结构清晰
   - 信息完整
   - 没有重复内容
5. 确保返回的是合法的JSON格式，不要添加任何额外说明"""

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

    def merge_knowledge(self, json_contents: list) -> dict:
        """合并多个JSON格式的知识内容"""
        try:
            # 将JSON内容列表转换为字符串
            json_str = json.dumps(json_contents, ensure_ascii=False)
            logger.info(f"Preparing to merge {len(json_contents)} JSON contents")
            logger.debug(f"Input contents: {json_str}")
            
            # 构建提示词
            messages = [
                {"role": "system", "content": MERGE_PROMPT},
                {"role": "user", "content": f"请合并以下JSON内容：{json_str}"}
            ]
            logger.debug(f"Prepared messages: {messages}")
            
            # 调用API
            logger.info("Making API call to Moonshot for knowledge merge...")
            try:
                response = self.client.chat.completions.create(
                    model="moonshot-v1-8k",
                    messages=messages,
                    temperature=0.1,
                    response_format={"type": "json_object"},
                    max_tokens=4000
                )
                logger.info("API call successful")
                
                # 获取响应文本
                response_text = response.choices[0].message.content
                logger.debug(f"Raw API Response: {response_text}")
                
                # 解析JSON响应
                try:
                    merged_knowledge = json.loads(response_text)
                    logger.info("Successfully parsed merged knowledge")
                    logger.debug(f"Parsed result: {merged_knowledge}")
                    
                    # 确保所有值都是数组格式
                    for key in merged_knowledge:
                        if not isinstance(merged_knowledge[key], list):
                            merged_knowledge[key] = [merged_knowledge[key]] if merged_knowledge[key] else []
                    
                    return merged_knowledge
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse merged JSON: {str(e)}")
                    logger.error(f"Invalid JSON response: {response_text}")
                    raise ValueError(f"Invalid JSON response from API: {str(e)}")
                    
            except Exception as e:
                logger.error(f"API call failed during merge: {str(e)}")
                logger.error(f"Full error details: {e}", exc_info=True)
                raise ValueError(f"API call failed: {str(e)}")
                
        except Exception as e:
            logger.error(f"Error in merge_knowledge: {str(e)}")
            logger.error("Full error traceback:", exc_info=True)
            raise
