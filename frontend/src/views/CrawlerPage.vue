<template>
  <div class="crawler-page">
    <div class="crawler-content">
      <h1 style="font-size: 2.5rem; font-weight: bold; margin-bottom: 1rem">智能网页内容分析</h1>
      <p class="subtitle">
        一键提取网页内容，实现快速、准确的知识获取
      </p>
      <WebCrawler />
    </div>
  </div>
</template>

<script setup lang="ts">
import WebCrawler from '../components/WebCrawler.vue'
</script>

<style scoped>
.crawler-page {
  min-height: calc(100vh - 60px);
  padding: 20px;
}

.crawler-content {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 2rem;
}
</style> 