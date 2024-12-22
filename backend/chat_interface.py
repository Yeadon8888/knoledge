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
.container {
    margin-top: 20px;
}
.chat-message {
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    font-size: 15px;
    line-height: 1.6;
}
.user-message {
    background-color: #e8f0fe;
    border-left: 4px solid #1a73e8;
}
.assistant-message {
    background-color: #f8f9fa;
    border-left: 4px solid #202124;
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
.disclaimer {
    font-size: 12px;
    color: #666;
    padding: 10px;
    background-color: #f5f5f5;
    border-radius: 5px;
    margin-top: 20px;
}
.header-text {
    text-align: center;
    margin-bottom: 20px;
}
.model-name {
    font-size: 24px;
    font-weight: bold;
    color: #1a237e;
    margin-bottom: 10px;
}
.model-description {
    color: #666;
    font-size: 14px;
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
        return "🔴 系统暂时无法处理您的法律咨询，请稍后再试。"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "❌ 很抱歉，处理您的咨询时遇到问题，请重新提问。"

def chat_response(message: str, history: List[Tuple[str, str]]) -> str:
    """
    处理聊天消息并返回响应
    """
    try:
        # 如果消息为空，返回提示
        if not message.strip():
            return "💡 请输入您的法律问题"
        
        # 获取答案
        response = query_backend(message)
        
        return response
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return "⚠️ 很抱歉，无法处理您的问题，请重新描述您的法律问题。"

# 创建Gradio界面
def create_chat_interface():
    """
    创建Gradio聊天界面
    """
    # 设置界面主题和样式
    theme = gr.themes.Base().set(
        body_background_fill="#f8f9fa",
        block_background_fill="#ffffff",
        block_border_width="0",
        block_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        button_primary_background_fill="#1a237e",
        button_primary_background_fill_hover="#283593",
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
        <div class="header-text">
            <div class="model-name">⚖️ Qwen2.5_7B_Instruct_Law</div>
            <div class="model-description">基于通义千问2.5的法律大模型，专注于提供准确、专业的法律咨询服务</div>
        </div>
        """)
        
        chatbot = gr.Chatbot(
            label="法律咨询对话",
            bubble_full_width=False,
            show_label=True,
            height=450
        )
        
        with gr.Row():
            txt = gr.Textbox(
                label="请描述您的法律问题",
                placeholder="请详细描述您的法律问题，我会为您提供专业的建议...",
                scale=8
            )
            submit_btn = gr.Button("发送", scale=1, variant="primary")
        
        clear_btn = gr.Button("🗑️ 清除对话记录")
        
        # 添加示例问题
        gr.Examples(
            examples=[
                "什么情况下可以主张正当防卫？",
                "签订劳动合同需要注意哪些问题？",
                "遇到交通事故该如何处理？",
                "房屋买卖合同纠纷如何解决？",
                "如何处理工伤赔偿问题？"
            ],
            inputs=txt,
            label="💡 常见法律问题示例"
        )
        
        # 添加免责声明
        gr.Markdown("""
        <div class="disclaimer">
        ⚠️ 免责声明：本系统提供的建议仅供参考，不构成正式的法律意见。具体法律问题请咨询专业律师。在处理重要法律事务时，建议您寻求专业律师的帮助。
        </div>
        """)
        
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
