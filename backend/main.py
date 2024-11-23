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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
