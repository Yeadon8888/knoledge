<template>
  <div class="hero-container">
    <!-- 顶部标题 -->
    <div class="hero-header" :class="{ 'fade-in': show }">
      <h1>Welcome to Our Amazing Platform</h1>
    </div>

    <!-- 中间说明区域 -->
    <div class="hero-content" :class="{ 'slide-up': show }">
      <el-row justify="center">
        <el-col :span="16">
          <div class="content-box">
            <h2>Transform Your Ideas into Reality</h2>
            <p>Our platform provides powerful tools and features to help you build amazing applications quickly and efficiently. Whether you're a developer, designer, or entrepreneur, we've got everything you need to succeed.</p>
            
            <div class="feature-grid">
              <div class="feature-item">
                <el-icon><Monitor /></el-icon>
                <h3>Modern UI</h3>
                <p>Beautiful and responsive design</p>
              </div>
              <div class="feature-item">
                <el-icon><Lightning /></el-icon>
                <h3>Fast API</h3>
                <p>High-performance backend</p>
              </div>
              <div class="feature-item">
                <el-icon><Connection /></el-icon>
                <h3>Real-time</h3>
                <p>Instant updates and sync</p>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 底部按钮 -->
    <div class="hero-footer" :class="{ 'fade-in': show }">
      <el-button type="primary" size="large" @click="handleGetStarted">
        Get Started
        <el-icon class="el-icon--right"><ArrowRight /></el-icon>
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Monitor, Lightning, Connection, ArrowRight } from '@element-plus/icons-vue'
import { ElNotification } from 'element-plus'

const show = ref(false)

onMounted(() => {
  // 添加一个小延迟来触发动画
  setTimeout(() => {
    show.value = true
  }, 100)
})

const handleGetStarted = () => {
  ElNotification({
    title: 'Welcome!',
    message: 'Thank you for getting started with our platform!',
    type: 'success',
  })
}
</script>

<style scoped>
.hero-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.hero-header {
  text-align: center;
  opacity: 0;
  transform: translateY(-20px);
}

.hero-header h1 {
  font-size: 3rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.hero-content {
  flex-grow: 1;
  display: flex;
  align-items: center;
  opacity: 0;
  transform: translateY(20px);
}

.content-box {
  text-align: center;
  padding: 2rem;
}

.content-box h2 {
  font-size: 2rem;
  color: #34495e;
  margin-bottom: 1.5rem;
}

.content-box p {
  font-size: 1.2rem;
  color: #5d6d7e;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 3rem;
}

.feature-item {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-5px);
}

.feature-item .el-icon {
  font-size: 2rem;
  color: #409EFF;
  margin-bottom: 1rem;
}

.feature-item h3 {
  font-size: 1.2rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.feature-item p {
  font-size: 1rem;
  color: #5d6d7e;
  margin: 0;
}

.hero-footer {
  text-align: center;
  margin-top: 2rem;
  opacity: 0;
}

/* 动画类 */
.fade-in {
  animation: fadeIn 1s ease forwards;
}

.slide-up {
  animation: slideUp 1s ease forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-header h1 {
    font-size: 2rem;
  }

  .content-box h2 {
    font-size: 1.5rem;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }
}
</style>
