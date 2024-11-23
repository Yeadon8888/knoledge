<template>
  <div class="hero-section" :class="{ 'tracked-in': isTrackedIn }">
    <div class="initial-content" v-if="!hasStarted">
      <h1 class="tracking-in-expand">多源知识融合与获取</h1>
      <p class="tracking-in-expand-delay">
        整合多个来源的知识，构建您的知识图谱
      </p>
      <button @click="startExplore" class="start-button">开始探索</button>
    </div>

    <div v-else class="main-content fade-in">
      <header class="header">
        <h2>知识获取平台</h2>
        <p class="subtitle">融合多源数据，构建个性化知识体系</p>
      </header>

      <div class="feature-cards">
        <div class="feature-card" @click="navigateToCrawler">
          <div class="card-icon">🕷️</div>
          <h3>网页爬虫</h3>
          <p>智能抓取网页内容，自动构建知识库</p>
        </div>

        <div class="feature-card">
          <div class="card-icon">🔄</div>
          <h3>知识融合</h3>
          <p>多源数据智能整合，构建知识图谱</p>
        </div>

        <div class="feature-card">
          <div class="card-icon">📊</div>
          <h3>知识管理</h3>
          <p>系统化整理和可视化展示</p>
        </div>

        <div class="feature-card">
          <div class="card-icon">🔍</div>
          <h3>智能检索</h3>
          <p>快速精准定位知识点</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const hasStarted = ref(false)
const isTrackedIn = ref(false)

setTimeout(() => {
  isTrackedIn.value = true
}, 100)

const startExplore = () => {
  hasStarted.value = true
}

const navigateToCrawler = () => {
  router.push('/crawler')
}
</script>

<style scoped>
.hero-section {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%);
  color: white;
  padding: 2rem;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s ease-out;
}

.hero-section.tracked-in {
  opacity: 1;
  transform: translateY(0);
}

.initial-content {
  text-align: center;
}

.tracking-in-expand {
  animation: tracking-in-expand 0.7s cubic-bezier(0.215, 0.610, 0.355, 1.000) both;
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

.tracking-in-expand-delay {
  animation: tracking-in-expand 0.7s cubic-bezier(0.215, 0.610, 0.355, 1.000) 0.5s both;
  font-size: 1.5rem;
  color: #a8a8a8;
  margin-bottom: 2rem;
}

.start-button {
  padding: 1rem 2.5rem;
  font-size: 1.2rem;
  background: #4CAF50;
  border: none;
  border-radius: 30px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  animation: fade-in 0.5s ease-out 1s both;
}

.start-button:hover {
  background: #45a049;
  transform: scale(1.05);
}

.main-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.fade-in {
  animation: fade-in 0.8s ease-out;
}

.header {
  text-align: center;
  margin-bottom: 4rem;
}

.header h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.2rem;
  color: #a8a8a8;
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  cursor: pointer;
}

.feature-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.15);
}

.card-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.feature-card p {
  color: #a8a8a8;
  line-height: 1.6;
}

@keyframes tracking-in-expand {
  0% {
    letter-spacing: -0.5em;
    opacity: 0;
  }
  40% {
    opacity: 0.6;
  }
  100% {
    opacity: 1;
  }
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 