import gradio as gr
import requests
import json
import logging
from typing import List, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI 后端地址
BACKEND_URL = "http://localhost:8001"

def format_response(response: str) -> str:
    """
    格式化API返回的响应
    这里可以根据需要添加更多的格式化规则
    """
    return response.strip()

def query_backend(message: str) -> str:
    """
    向后端API发送查询请求
    """
    try:
        response = requests.post(
            f"{BACKEND_URL}/search",
            json={"query": message},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return format_response(response.json()["result"])
    except requests.exceptions.RequestException as e:
        logger.error(f"Backend request failed: {str(e)}")
        return "抱歉，服务器暂时无法响应，请稍后再试。"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "抱歉，发生了意外错误，请稍后重试。"

def chat_response(message: str, history: List[Tuple[str, str]]) -> str:
    """
    处理聊天消息并返回响应
    """
    try:
        # 如果消息为空，返回提示
        if not message.strip():
            return "请输入您的问题"
        
        # 获取答案
        response = query_backend(message)
        
        return response
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return "抱歉，处理您的问题时出现错误，请重试。"

# 创建Gradio界面
def create_chat_interface():
    """
    创建Gradio聊天界面
    """
    # 设置界面主题和样式
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="gray",
    )
    
    # 创建聊天界面
    chat_interface = gr.ChatInterface(
        fn=chat_response,
        title="智能知识助手",
        description="您好！我是您的知识管理助手，请告诉我您想了解什么？",
        theme=theme,
        examples=[
            ["什么是机器学习？"],
            ["Python和Java的主要区别是什么？"],
            ["如何提高编程效率？"]
        ]
    )
    
    return chat_interface

if __name__ == "__main__":
    # 创建并启动聊天界面
    chat_interface = create_chat_interface()
    chat_interface.launch(
        server_name="0.0.0.0",  # 允许外部访问
        server_port=7860,       # 使用7860端口
        share=False,            # 不创建公共链接
        debug=True             # 启用调试模式
    )
