&lt;template>
  &lt;div class="search-container">
    &lt;el-card class="search-card">
      &lt;div class="search-header">
        &lt;h2>智能知识检索&lt;/h2>
        &lt;p>输入您的问题，AI将帮您找到相关知识&lt;/p>
      &lt;/div>

      &lt;div class="search-input">
        &lt;el-input
          v-model="searchQuery"
          type="textarea"
          :rows="3"
          placeholder="请输入您的问题..."
          @keyup.enter="handleSearch"
        />
        &lt;el-button 
          type="primary" 
          :loading="loading"
          @click="handleSearch"
          class="search-button"
        >
          搜索
        &lt;/el-button>
      &lt;/div>

      &lt;div v-if="searchResult" class="search-result">
        &lt;el-divider>搜索结果&lt;/el-divider>
        &lt;div class="result-content">
          &lt;div v-html="formattedResult">&lt;/div>
        &lt;/div>
      &lt;/div>
    &lt;/el-card>
  &lt;/div>
&lt;/template>

&lt;script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import DOMPurify from 'dompurify'
import { marked } from 'marked'

const searchQuery = ref('')
const searchResult = ref('')
const loading = ref(false)

const formattedResult = computed(() => {
  if (!searchResult.value) return ''
  // 使用marked将Markdown转换为HTML，并用DOMPurify清理
  return DOMPurify.sanitize(marked(searchResult.value))
})

const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    ElMessage.warning('请输入搜索内容')
    return
  }

  loading.value = true
  try {
    const response = await axios.post('http://localhost:8001/search', {
      query: searchQuery.value
    })
    searchResult.value = response.data.result
  } catch (error) {
    ElMessage.error('搜索失败，请稍后重试')
    console.error('Search error:', error)
  } finally {
    loading.value = false
  }
}
&lt;/script>

&lt;style scoped>
.search-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.search-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
}

.search-header {
  text-align: center;
  margin-bottom: 20px;
}

.search-header h2 {
  color: #409EFF;
  margin-bottom: 10px;
}

.search-header p {
  color: #666;
  font-size: 14px;
}

.search-input {
  margin-bottom: 20px;
}

.search-button {
  width: 100%;
  margin-top: 10px;
}

.search-result {
  margin-top: 20px;
}

.result-content {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
  line-height: 1.6;
}

:deep(.el-card__body) {
  padding: 30px;
}
&lt;/style>
