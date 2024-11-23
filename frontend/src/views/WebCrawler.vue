<template>
  <div class="crawler-page">
    <WebCrawler />
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
</style> 