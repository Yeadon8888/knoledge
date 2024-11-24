from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import chardet
import logging
import os
from dotenv import load_dotenv
from moonshot_api import MoonshotAPI

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 从环境变量获取API密钥
load_dotenv()
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
if not MOONSHOT_API_KEY:
    logger.error("MOONSHOT_API_KEY not found in environment variables!")
else:
    logger.info("MOONSHOT_API_KEY loaded successfully")

app = FastAPI()
moonshot = MoonshotAPI(MOONSHOT_API_KEY)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置为具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CrawlRequest(BaseModel):
    url: str

class CrawlResponse(BaseModel):
    title: str
    content: str

class ExtractRequest(BaseModel):
    content: str

class ExtractResponse(BaseModel):
    keywords: dict

class MergeRequest(BaseModel):
    contents: list[dict]

class MergeResponse(BaseModel):
    result: dict

class MindmapRequest(BaseModel):
    json_data: dict

class MindmapResponse(BaseModel):
    mindmap_data: dict

def extract_content(html_content: str) -> tuple:
    """从HTML中提取标题和正文内容"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 提取标题
    title = ""
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.text.strip()
    
    # 提取正文内容
    # 移除script和style元素
    for script in soup(["script", "style"]):
        script.decompose()
    
    # 获取文本
    text = soup.get_text()
    
    # 断行
    lines = (line.strip() for line in text.splitlines())
    
    # 去除空行和多余空格
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    content = ' '.join(chunk for chunk in chunks if chunk)
    
    return title, content

def convert_to_mindmap(data: dict, parent_id: str = "root") -> dict:
    """将JSON数据转换为脑图数据结构"""
    nodes = []
    edges = []
    
    # 创建根节点
    root_node = {
        "id": parent_id,
        "label": "知识地图",
        "style": {
            "fill": "#91d5ff",
            "stroke": "#40a9ff"
        }
    }
    nodes.append(root_node)
    
    def process_value(key: str, value: any, parent_id: str, index: int):
        node_id = f"{parent_id}-{index}"
        
        # 创建键节点
        key_node = {
            "id": node_id,
            "label": str(key),
            "style": {
                "fill": "#d9f7be",
                "stroke": "#73d13d"
            }
        }
        nodes.append(key_node)
        
        # 创建与父节点的连接
        edges.append({
            "source": parent_id,
            "target": node_id,
            "style": {
                "stroke": "#91d5ff",
                "endArrow": True
            }
        })
        
        # 处理值
        if isinstance(value, (list, tuple)):
            for i, item in enumerate(value):
                leaf_id = f"{node_id}-{i}"
                leaf_node = {
                    "id": leaf_id,
                    "label": str(item),
                    "style": {
                        "fill": "#ffd6e7",
                        "stroke": "#ff85c0"
                    }
                }
                nodes.append(leaf_node)
                edges.append({
                    "source": node_id,
                    "target": leaf_id,
                    "style": {
                        "stroke": "#73d13d",
                        "endArrow": True
                    }
                })
        elif isinstance(value, dict):
            for i, (k, v) in enumerate(value.items()):
                process_value(k, v, node_id, i)
        else:
            leaf_id = f"{node_id}-value"
            leaf_node = {
                "id": leaf_id,
                "label": str(value),
                "style": {
                    "fill": "#ffd6e7",
                    "stroke": "#ff85c0"
                }
            }
            nodes.append(leaf_node)
            edges.append({
                "source": node_id,
                "target": leaf_id,
                "style": {
                    "stroke": "#73d13d",
                    "endArrow": True
                }
            })
    
    # 处理每个顶层键值对
    for i, (key, value) in enumerate(data.items()):
        process_value(key, value, parent_id, i)
    
    return {
        "nodes": nodes,
        "edges": edges
    }

@app.get("/health")
async def health_check():
    return {"status": "Backend is healthy!"}

@app.post("/crawl")
async def crawl(request: CrawlRequest):
    try:
        logger.info(f"Received crawl request for URL: {request.url}")
        
        # 发送HTTP请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        logger.debug("Sending HTTP request...")
        
        # 使用aiohttp进行异步请求
        async with aiohttp.ClientSession() as session:
            async with session.get(request.url, headers=headers, timeout=30) as response:
                logger.info(f"Got response with status code: {response.status}")
                
                # 限制内容大小为10MB
                MAX_SIZE = 10 * 1024 * 1024  # 10MB
                content = await response.read()
                if len(content) > MAX_SIZE:
                    raise HTTPException(status_code=413, detail="Content too large")
                
                # 检测编码
                encodings = chardet.detect(content)
                encoding = encodings['encoding'] if encodings['encoding'] else 'utf-8'
                text = content.decode(encoding)
                logger.debug(f"Using encoding: {encoding}")
                
                # 提取内容
                title, content = extract_content(text)
                if len(content) < 10:  # 内容太少，可能是无效页面
                    raise HTTPException(status_code=422, detail="Invalid page content")
                    
                logger.info(f"Extracted title: {title[:50]}...")
                logger.debug(f"Content length: {len(content)} characters")
                
                return CrawlResponse(
                    title=title,
                    content=content
                )
        
    except asyncio.TimeoutError:
        logger.error("Request timeout")
        raise HTTPException(status_code=504, detail="Request timeout")
    except aiohttp.ClientError as e:
        logger.error(f"Network error: {str(e)}")
        raise HTTPException(status_code=502, detail="Network error")
    except Exception as e:
        logger.error(f"Error crawling URL: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract")
async def extract(request: ExtractRequest):
    try:
        logger.info("Starting content extraction...")
        # 使用MoonshotAPI提取关键词
        keywords = moonshot.extract_knowledge(request.content[:4000])  # 限制内容长度
        logger.info("Keywords extraction completed")
        
        return ExtractResponse(keywords=keywords)
    except Exception as e:
        logger.error(f"Error extracting content: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/merge", response_model=MergeResponse)
async def merge(request: MergeRequest):
    """合并多个JSON格式的知识内容"""
    try:
        logger.info(f"Received merge request with {len(request.contents)} items")
        logger.debug(f"Request contents: {request.contents}")
        
        # 验证输入数据
        if not request.contents:
            raise HTTPException(status_code=400, detail="No content provided")
            
        # 确保所有内容都是字典类型
        contents = []
        for item in request.contents:
            if not isinstance(item, dict):
                logger.error(f"Invalid content type: {type(item)}")
                raise HTTPException(status_code=400, detail="All contents must be JSON objects")
            contents.append(item)
        
        # 调用API进行合并
        result = moonshot.merge_knowledge(contents)
        logger.info("Successfully merged contents")
        logger.debug(f"Merge result: {result}")
        
        return MergeResponse(result=result)
    except Exception as e:
        logger.error(f"Error in merge: {str(e)}", exc_info=True)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mindmap")
async def create_mindmap(request: MindmapRequest):
    """将JSON知识内容转换为脑图数据结构"""
    try:
        logger.info("Converting JSON to mindmap structure")
        mindmap_data = convert_to_mindmap(request.json_data)
        return MindmapResponse(mindmap_data=mindmap_data)
    except Exception as e:
        logger.error(f"Error creating mindmap: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
