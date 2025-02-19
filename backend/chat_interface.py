import gradio as gr
import requests
import json
import logging
from typing import List, Tuple
from deepseek_api import DeepSeekAPI

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 初始化DeepSeek API
deepseek = DeepSeekAPI()

# FastAPI 后端地址
BACKEND_URL = "http://localhost:8001"

# 示例法律条文数据
SAMPLE_LAW_DATA = {
    "第十九条": {
        "title": "《中华人民共和国劳动合同法》",
        "contents": "第十九条【试用期】劳动合同期限三个月以上不满一年的，试用期不得超过一个月；劳动合同期限一年以上不满三年的，试用期不得超过二个月；三年以上固定期限和无固定期限的劳动合同，试用期不得超过六个月。同一用人单位与同一劳动者只能约定一次试用期。以完成一定工作任务为期限的劳动合同或者劳动合同期限不满三个月的，不得约定试用期。试用期包含在劳动合同期限内。劳动合同仅约定试用期的，试用期不成立，该期限为劳动合同期限。"
    },
    "第二十条": {
        "title": "《中华人民共和国劳动合同法》",
        "contents": "第二十条【工资约定】劳动合同应当具备以下条款：（一）用人单位的名称、住所和法定代表人或者主要负责人；（二）劳动者的姓名、住址和居民身份证或者其他有效身份证件号码；（三）劳动合同期限；（四）工作内容和工作地点；（五）工作时间和休息休假；（六）劳动报酬；（七）社会保险；（八）劳动保护、劳动条件和职业危害防护；（九）法律、法规规定应当纳入劳动合同的其他事项。"
    },
    "第三十六条": {
        "title": "《中华人民共和国劳动合同法》",
        "contents": "第三十六条【工作时间】国家实行劳动者每日工作时间不超过八小时、平均每周工作时间不超过四十四小时的工时制度。"
    },
    "第四十六条": {
        "title": "《中华人民共和国劳动合同法》",
        "contents": "第四十六条【经济补偿】有下列情形之一的，用人单位应当向劳动者支付经济补偿：（一）劳动者依照本法第三十八条规定解除劳动合同的；（二）用人单位依照本法第三十六条规定向劳动者提出解除劳动合同并与劳动者协商一致解除劳动合同的；（三）用人单位依照本法第四十条规定解除劳动合同的；（四）用人单位依照本法第四十一条第一款规定解除劳动合同的；（五）除用人单位维持或者提高劳动合同约定条件续订劳动合同，劳动者不同意续订的情形外，依照本法第四十四条第一项规定终止固定期限劳动合同的；（六）依照本法第四十四条第四项、第五项规定终止劳动合同的；（七）法律、行政法规规定的其他情形。"
    },
    "第八十二条": {
        "title": "《中华人民共和国劳动合同法》",
        "contents": "第八十二条【违法解除赔偿】用人单位自用工之日起超过一个月不满一年未与劳动者订立书面劳动合同的，应当向劳动者每月支付二倍的工资。用人单位违反本法规定不与劳动者订立无固定期限劳动合同的，自应当订立无固定期限劳动合同之日起向劳动者每月支付二倍的工资。"
    }
}

def format_law_response(law_data: dict) -> str:
    """
    格式化法律条文响应
    """
    return f"""📖 {law_data['title']}

{law_data['contents']}

💡 法条解读：
1. 试用期长短与合同期限相关：
   - 3个月以上不满1年：试用期最长1个月
   - 1年以上不满3年：试用期最长2个月
   - 3年以上或无固定期限：试用期最长6个月

2. 重要限制：
   - 同一用人单位对同一劳动者只能约定一次试用期
   - 短期合同（不满3个月）不得约定试用期
   - 试用期必须包含在劳动合同期限内

3. 特别说明：
   - 如果合同只约定试用期，则试用期不成立
   - 该期限将被视为劳动合同期限
"""

def chat_response(message: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
    """
    处理聊天消息并返回响应
    """
    try:
        # 获取DeepSeek的回答
        response = deepseek.get_knowledge_response(message)
        
        # 更新历史记录
        history.append((message, response))
        return "", history
        
    except Exception as e:
        logger.error(f"聊天响应失败: {str(e)}")
        error_message = "抱歉，我暂时无法回答您的问题。请稍后再试。"
        history.append((message, error_message))
        return "", history

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
            <div class="model-name">🤖 智能知识助手</div>
            <div class="model-description">基于DeepSeek R1的智能知识管理助手，为您提供专业的知识管理服务</div>
        </div>
        """)
        
        chatbot = gr.Chatbot(
            label="知识管理对话",
            bubble_full_width=False,
            show_label=True,
            height=450
        )
        
        with gr.Row():
            txt = gr.Textbox(
                label="请输入您的问题",
                placeholder="请描述您的问题，我会为您提供专业的建议...",
                scale=8
            )
            submit_btn = gr.Button("发送", scale=1, variant="primary")
        
        clear_btn = gr.Button("🗑️ 清除对话记录")
        
        # 添加示例问题
        gr.Examples(
            examples=[
                "如何有效地组织和管理我的知识？",
                "请推荐一些好用的知识管理工具",
                "如何建立个人知识体系？",
                "如何提高学习效率？",
                "如何做好知识的分类和标签管理？"
            ],
            inputs=txt,
            label="💡 示例问题"
        )
        
        # 添加免责声明
        gr.Markdown("""
        <div class="disclaimer">
        ⚠️ 免责声明：本系统提供的建议仅供参考。在处理重要事务时，请结合实际情况谨慎判断。
        </div>
        """)
        
        # 设置事件处理
        txt.submit(chat_response, [txt, chatbot], [txt, chatbot])
        submit_btn.click(chat_response, [txt, chatbot], [txt, chatbot])
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
