<template>
  <div class="crawler-container">
    <el-card class="crawler-card">
      <template #header>
        <div class="card-header">
          <h2>Web Crawler</h2>
        </div>
      </template>
      
      <el-form :model="form" @submit.prevent="handleSubmit">
        <el-form-item>
          <el-input
            v-model="form.url"
            placeholder="Enter URL to crawl (e.g., https://example.com)"
            :prefix-icon="Link"
            clearable
          />
        </el-form-item>
        
        <el-form-item>
          <el-input
            v-model="form.selector"
            placeholder="CSS Selector (optional, e.g., .article-content)"
            :prefix-icon="Select"
            clearable
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            @click="handleSubmit" 
            :loading="loading"
            :icon="Download"
          >
            Crawl Website
          </el-button>
        </el-form-item>
      </el-form>

      <!-- Results Section -->
      <div v-if="result" class="results-section">
        <el-divider>Results</el-divider>
        
        <div class="result-item">
          <h3>Title</h3>
          <p>{{ result.title }}</p>
        </div>
        
        <div class="result-item">
          <h3>Content</h3>
          <el-scrollbar height="200px">
            <p class="content-text">{{ result.content }}</p>
          </el-scrollbar>
        </div>
        
        <div class="result-item">
          <h3>Links Found</h3>
          <el-scrollbar height="150px">
            <ul class="links-list">
              <li v-for="(link, index) in result.links" :key="index">
                <el-link :href="link" target="_blank" type="primary">{{ link }}</el-link>
              </li>
            </ul>
          </el-scrollbar>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { Link, Select, Download } from '@element-plus/icons-vue'
import { ElNotification } from 'element-plus'
import axios from 'axios'

const form = reactive({
  url: '',
  selector: ''
})

const loading = ref(false)
const result = ref(null)

const handleSubmit = async () => {
  if (!form.url) {
    ElNotification({
      title: 'Error',
      message: 'Please enter a URL',
      type: 'error',
    })
    return
  }

  loading.value = true
  try {
    const response = await axios.post('http://localhost:8001/crawl', {
      url: form.url,
      selector: form.selector || undefined
    })
    
    result.value = response.data
    
    ElNotification({
      title: 'Success',
      message: 'Website crawled successfully!',
      type: 'success',
    })
  } catch (error) {
    ElNotification({
      title: 'Error',
      message: error.response?.data?.detail || 'Failed to crawl website',
      type: 'error',
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.crawler-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.crawler-card {
  border-radius: 8px;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0;
  color: #2c3e50;
}

.results-section {
  margin-top: 2rem;
}

.result-item {
  margin-bottom: 1.5rem;
}

.result-item h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.content-text {
  white-space: pre-wrap;
  word-break: break-word;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.links-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.links-list li {
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #eee;
}

.links-list li:last-child {
  border-bottom: none;
}
</style>
