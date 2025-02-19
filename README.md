# 知识管理系统

这是一个基于 AI 的知识管理系统，支持网页内容爬取、知识提取、知识合并、知识图谱生成等功能。

## 功能特点

### 1. 网页爬取
- 支持从任意 URL 爬取网页内容
- 自动处理各种编码格式
- 智能提取网页标题和正文

### 2. 知识提取
- 使用 AI 技术从文本中提取结构化知识
- 自动识别关键信息类别
- 生成标准 JSON 格式输出

### 3. 知识合并
- 智能合并多个知识点
- 自动去重和整合
- 保持信息完整性

### 4. 知识图谱
- 生成可视化知识图谱
- 支持自定义节点样式
- 直观展示知识结构

### 5. 知识搜索
- 支持语义化搜索
- 快速定位相关知识
- 精准匹配内容

## 技术栈

### 前端
- Vue 3
- TypeScript
- Element Plus
- Vite

### 后端
- Python 3.8+
- FastAPI
- Moonshot API
- BeautifulSoup4

## 安装说明

### 前端安装
```bash
cd frontend
npm install
npm run dev
```

### 后端安装
```bash
cd backend
pip install -r requirements.txt
python main.py
```

## 环境配置

### 前端环境变量 (.env)
```
VITE_API_BASE_URL=http://localhost:8000
```

### 后端环境变量 (.env)
```
MOONSHOT_API_KEY=your_api_key_here
```

## API 文档

### 1. 爬取网页
```
POST /crawl
Request: { "url": "网页地址" }
Response: { "title": "标题", "content": "内容" }
```

### 2. 提取知识
```
POST /extract
Request: { "content": "文本内容" }
Response: { "keywords": { ... } }
```

### 3. 合并知识
```
POST /merge
Request: { "contents": [{...}, {...}] }
Response: { "result": {...} }
```

### 4. 生成知识图谱
```
POST /mindmap
Request: { "json_data": {...} }
Response: { "mindmap_data": {...} }
```

### 5. 搜索知识
```
POST /search
Request: { "query": "搜索关键词" }
Response: { "result": "搜索结果" }
```

## 开发计划

### 近期计划
1. 添加数据库支持
2. 实现用户认证系统
3. 添加缓存层
4. 完善测试用例
5. 添加监控系统

### 长期计划
1. 支持更多知识源
2. 优化知识提取算法
3. 增强知识图谱功能
4. 添加协作功能
5. 支持知识导出导入

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 许可证

MIT License
