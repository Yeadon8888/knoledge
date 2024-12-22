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

# 自定义CSS样式
custom_css = """
.gradio-container {
    max-width: 880px !important;
    margin: auto;
}
.chat-message {
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.user-message {
    background-color: #e3f2fd;
}
.assistant-message {
    background-color: #f5f5f5;
}
.message-container {
    margin: 15px 0;
}
.error-message {
    color: #d32f2f;
    padding: 10px;
    border-radius: 5px;
    background-color: #ffebee;
    margin: 10px 0;
}
"""

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
        return "🔴 抱歉，服务器暂时无法响应，请稍后再试。"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "❌ 抱歉，发生了意外错误，请稍后重试。"

def chat_response(message: str, history: List[Tuple[str, str]]) -> str:
    """
    处理聊天消息并返回响应
    """
    try:
        # 如果消息为空，返回提示
        if not message.strip():
            return "💡 请输入您的问题"
        
        # 获取答案
        response = query_backend(message)
        
        return response
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return "⚠️ 抱歉，处理您的问题时出现错误，请重试。"

# 创建Gradio界面
def create_chat_interface():
    """
    创建Gradio聊天界面
    """
    # 设置界面主题和样式
    theme = gr.themes.Base().set(
        body_background_fill="#f7f9fc",
        block_background_fill="#ffffff",
        block_border_width="0",
        block_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        button_primary_background_fill="#2196f3",
        button_primary_background_fill_hover="#1976d2",
        button_primary_text_color="#ffffff",
        input_background_fill="#ffffff",
        input_border_color="#e0e0e0",
        input_border_width="1px",
        input_padding="12px",
        input_radius="8px",
        input_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    )
    
    # 创建聊天界面
    with gr.Blocks(theme=theme, css=custom_css) as chat_interface:
        gr.Markdown("""
        # 🤖 智能知识助手
        
        您好！我是您的知识管理助手，请告诉我您想了解什么？
        """)
        
        chatbot = gr.Chatbot(
            label="对话历史",
            bubble_full_width=False,
            show_label=True,
            height=400
        )
        
        with gr.Row():
            txt = gr.Textbox(
                label="输入您的问题",
                placeholder="请输入您的问题，按回车发送...",
                scale=8
            )
            submit_btn = gr.Button("发送", scale=1, variant="primary")
        
        clear_btn = gr.Button("🗑️ 清除对话")
        
        # 添加示例问题
        gr.Examples(
            examples=[
                "什么是机器学习？",
                "Python和Java的主要区别是什么？",
                "如何提高编程效率？"
            ],
            inputs=txt,
            label="💡 示例问题"
        )
        
        # 设置事件处理
        txt.submit(chat_response, [txt, chatbot], [chatbot])
        submit_btn.click(chat_response, [txt, chatbot], [chatbot])
        clear_btn.click(lambda: None, None, chatbot, queue=False)
        
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
