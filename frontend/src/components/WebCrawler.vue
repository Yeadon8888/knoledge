<!-- WebCrawler.vue -->
<template>
  <div class="web-crawler">
    <!-- 头部区域 -->
    <header class="header">
      <h1>网页内容智能分析</h1>
      <p class="subtitle">输入网址，一键提取关键信息</p>
    </header>

    <!-- 输入区域 -->
    <el-card class="input-section" :body-style="{ padding: '20px' }">
      <div class="url-input">
        <el-input
          v-model="url"
          placeholder="请输入网页URL（例如：https://www.example.com）"
          :disabled="loading"
          @keyup.enter="extractKnowledge"
          size="large"
          clearable
        >
          <template #prefix>
            <el-icon><Document /></el-icon>
          </template>
          <template #append>
            <el-button
              type="primary"
              @click="extractKnowledge"
              :loading="loading"
              :icon="loading ? 'Loading' : 'Search'"
            >
              {{ loading ? '分析中...' : '提取信息' }}
            </el-button>
          </template>
        </el-input>
      </div>
    </el-card>

    <!-- 错误提示 -->
    <el-alert
      v-if="error"
      :title="error"
      type="error"
      :closable="true"
      show-icon
      class="my-4"
      @close="error = ''"
    />

    <!-- 加载动画 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>

    <!-- 结果展示 -->
    <transition name="fade">
      <div v-if="hasResults" class="results">
        <!-- 标题卡片 -->
        <el-card v-if="title" class="result-card">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>页面标题</span>
            </div>
          </template>
          <div class="title-content">{{ title }}</div>
        </el-card>

        <!-- 知识分析结果 -->
        <el-card v-if="content" class="result-card knowledge-card">
          <template #header>
            <div class="card-header">
              <el-icon><Connection /></el-icon>
              <span>知识分析</span>
              <el-button v-if="knowledge" type="primary" link @click="copyKnowledge">
                复制结果
              </el-button>
            </div>
          </template>
          <div v-if="extracting" class="extracting-status">
            <el-skeleton :rows="6" animated />
            <div class="extracting-text">正在分析内容，请稍候...</div>
          </div>
          <div v-else-if="knowledge" class="knowledge-grid">
            <div
              v-for="(value, key) in knowledge"
              :key="key"
              class="knowledge-item"
            >
              <h4>{{ key }}</h4>
              <el-tag
                v-for="(item, index) in value"
                :key="index"
                class="knowledge-tag"
                :type="getTagType(index)"
              >
                {{ item }}
              </el-tag>
            </div>
          </div>
          <div v-else class="no-knowledge">
            暂无分析结果
          </div>
        </el-card>

        <!-- 原始内容 -->
        <el-card v-if="content" class="result-card">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>原始内容</span>
              <el-button type="primary" link @click="showContent = !showContent">
                {{ showContent ? '收起' : '展开' }}
              </el-button>
            </div>
          </template>
          <div v-show="showContent" class="content-text">
            {{ content }}
          </div>
        </el-card>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, Connection } from '@element-plus/icons-vue'
import axios from 'axios'

const url = ref('')
const loading = ref(false)
const extracting = ref(false)
const error = ref('')
const title = ref('')
const content = ref('')
const knowledge = ref(null)
const showContent = ref(false)
const stats = ref({})

const hasResults = computed(() => title.value || content.value || knowledge.value)

const tagTypes = ['', 'success', 'warning', 'danger', 'info']
const getTagType = (index) => tagTypes[index % tagTypes.length]

const copyKnowledge = async () => {
  try {
    await navigator.clipboard.writeText(JSON.stringify(knowledge.value, null, 2))
    ElMessage.success('已复制到剪贴板')
  } catch (err) {
    ElMessage.error('复制失败')
  }
}

const extractKnowledge = async () => {
  if (!url.value) {
    ElMessage.warning('请输入URL')
    return
  }

  if (!url.value.startsWith('http')) {
    url.value = 'http://' + url.value
  }

  loading.value = true
  error.value = ''
  title.value = ''
  content.value = ''
  knowledge.value = null
  showContent.value = false

  try {
    // 检查后端健康状态
    try {
      await axios.get('http://localhost:8001/health', { timeout: 5000 })
    } catch (err) {
      throw new Error('后端服务未启动或无法访问，请检查后端服务状态')
    }

    // 发送爬取请求
    ElMessage.info('开始爬取网页内容...')
    const crawlResponse = await retryOperation(async () => {
      return await axios.post('http://localhost:8001/crawl', {
        url: url.value
      }, {
        timeout: 30000  // 30秒超时
      })
    }, 3, 2000)  // 最多重试3次，间隔2秒

    if (crawlResponse.data) {
      title.value = crawlResponse.data.title || ''
      content.value = crawlResponse.data.content || ''
      ElMessage.success('网页内容爬取成功！')
      
      // 开始提取内容
      extracting.value = true
      ElMessage.info('正在分析网页内容...')
      
      try {
        const extractResponse = await axios.post('http://localhost:8001/extract', {
          content: content.value
        }, {
          timeout: 60000  // 60秒超时
        })
        
        if (extractResponse.data) {
          knowledge.value = extractResponse.data.keywords
          if (!knowledge.value) {
            error.value = '无法提取知识，请检查内容是否有效'
            ElMessage.warning('无法从网页提取有效知识')
          } else {
            ElMessage.success('知识提取成功！')
            // 更新统计信息
            await updateStats()
          }
        }
      } catch (err) {
        console.error('Error extracting content:', err)
        error.value = '内容提取失败：' + (err.response?.data?.detail || err.message)
        ElMessage.error('内容提取失败')
      } finally {
        extracting.value = false
      }
    }
  } catch (err) {
    console.error('Error:', err)
    let errorMessage = '请求失败'
    
    if (err.response) {
      switch (err.response.status) {
        case 404:
          errorMessage = '网页不存在'
          break
        case 413:
          errorMessage = '网页内容过大'
          break
        case 422:
          errorMessage = '无效的网页内容'
          break
        case 502:
          errorMessage = '网络错误'
          break
        case 504:
          errorMessage = '请求超时'
          break
        default:
          errorMessage = err.response.data?.detail || '未知错误'
      }
    } else if (err.message) {
      errorMessage = err.message
    }
    
    error.value = errorMessage
    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}

// 添加自动重试机制
const retryOperation = async (operation, maxRetries = 3, delay = 1000) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await operation()
    } catch (err) {
      if (i === maxRetries - 1) throw err
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }
}

// 更新统计信息
const updateStats = async () => {
  try {
    const response = await retryOperation(() => 
      axios.get('http://localhost:8001/knowledge')
    )
    const knowledge = response.data.knowledge || {}
    stats.value = {
      pageCount: knowledge.page_count || 0,
      knowledgeCount: knowledge.knowledge_count || 0,
      categoryCount: knowledge.category_count || 0
    }
  } catch (err) {
    console.error('Failed to fetch stats:', err)
    ElMessage.warning('无法获取知识库统计信息')
  }
}

// 搜索知识
const searchKnowledge = async () => {
  if (!searchQuery.value) {
    ElMessage.warning('请输入搜索关键词')
    return
  }

  searchLoading.value = true
  try {
    const response = await retryOperation(() =>
      axios.post('http://localhost:8001/search', {
        query: searchQuery.value
      })
    )
    searchResults.value = response.data.results || []
    
    if (searchResults.value.length === 0) {
      ElMessage.info('未找到相关知识')
    } else {
      ElMessage.success(`找到 ${searchResults.value.length} 条相关知识`)
    }
  } catch (err) {
    console.error('Search error:', err)
    ElMessage.error('搜索失败，请稍后重试')
    searchResults.value = []
  } finally {
    searchLoading.value = false
  }
}
</script>

<style scoped>
.web-crawler {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  color: var(--el-color-primary);
  margin: 0;
  font-size: 2rem;
}
  
.subtitle {
  color: var(--el-text-color-secondary);
  margin: 0.5rem 0;
}

.input-section {
  margin-bottom: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.url-input {
  width: 100%;
}

.loading-container {
  margin: 2rem 0;
}

.results {
  margin-top: 2rem;
}

.result-card {
  margin-bottom: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.result-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-header .el-icon {
  font-size: 1.2em;
  color: var(--el-color-primary);
}

.title-content {
  font-size: 1.1em;
  color: var(--el-text-color-primary);
}

.knowledge-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.knowledge-item {
  background: var(--el-bg-color-page);
  padding: 1rem;
  border-radius: 6px;
  border: 1px solid var(--el-border-color-lighter);
}

.knowledge-item h4 {
  margin: 0 0 0.8rem 0;
  color: var(--el-color-primary);
  font-size: 1rem;
}

.knowledge-tag {
  margin: 0.3rem;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.content-text {
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 0.95em;
  line-height: 1.6;
  color: var(--el-text-color-regular);
  padding: 0.5rem;
  max-height: 500px;
  overflow-y: auto;
}

.extracting-status {
  padding: 20px;
  text-align: center;
}

.extracting-text {
  margin-top: 20px;
  color: #909399;
  font-size: 14px;
}

.no-knowledge {
  padding: 20px;
  text-align: center;
  color: #909399;
  font-size: 14px;
}

/* 搜索部分样式 */
.search-section {
  margin-top: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.search-input {
  margin-bottom: 1.5rem;
}

.search-results {
  margin-top: 1.5rem;
}

.knowledge-stats {
  margin-top: 2rem;
  padding: 1rem;
  background: var(--el-bg-color-page);
  border-radius: 8px;
}

/* 表格样式优化 */
.el-table {
  --el-table-border-color: var(--el-border-color-lighter);
  --el-table-header-bg-color: var(--el-bg-color-page);
  border-radius: 8px;
  overflow: hidden;
}

.el-table th {
  background-color: var(--el-bg-color-page);
  font-weight: 600;
}

.el-table .el-tag {
  display: inline-flex;
  align-items: center;
}

/* 进度条样式优化 */
.el-progress {
  margin: 0;
  padding: 0;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .web-crawler {
    padding: 10px;
  }

  .header h1 {
    font-size: 1.5rem;
  }

  .knowledge-grid {
    grid-template-columns: 1fr;
  }

  .el-descriptions {
    width: 100%;
  }
}

/* 暗黑模式适配 */
:root[class~="dark"] {
  .knowledge-item,
  .knowledge-stats {
    background: var(--el-bg-color);
  }

  .el-table th {
    background-color: var(--el-bg-color);
  }
}
</style>