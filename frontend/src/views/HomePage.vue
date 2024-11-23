<template>
  <div class="home-container">
    <div class="background-pattern"></div>
    <div class="background-gradient"></div>
    <div class="background-animation">
      <div v-for="n in 50" :key="n" class="floating-particle"></div>
    </div>
    
    <nav class="top-nav">
      <div class="logo">
        <div class="logo-mark">K</div>
        <span class="logo-text">Knowledge</span>
      </div>
      <div class="nav-links">
        <router-link to="/about">
          <i class="fas fa-info-circle"></i> 关于
        </router-link>
        <router-link to="/docs">
          <i class="fas fa-book"></i> 文档
        </router-link>
      </div>
    </nav>

    <main class="main-content">
      <div class="hero-section">
        <h1 class="title">多源知识融合与获取</h1>
        <p class="subtitle">整合多个来源的知识，构建您的知识图谱</p>
        
        <div class="stats-row">
          <div class="stat-item" v-for="(value, key) in statsData" :key="key">
            <div class="stat-number" ref="statNumbers">
              <span class="number">{{ value.current }}</span>+
            </div>
            <div class="stat-label">{{ value.label }}</div>
          </div>
        </div>

        <button class="cta-button" @click="startExplore">
          开始探索
          <span class="arrow">→</span>
        </button>
      </div>

      <div class="features-grid">
        <div v-for="feature in features" 
             :key="feature.title"
             class="feature-card"
             @mousemove="handleCardHover"
             @mouseleave="handleCardLeave"
             @click="feature.action">
          <div class="feature-content">
            <div class="feature-icon" :class="feature.iconClass">
              <i :class="feature.icon"></i>
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
          <div class="card-shine"></div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

interface StatItem {
  current: number
  target: number
  label: string
}

interface StatsData {
  sources: StatItem
  users: StatItem
  graphs: StatItem
}

const statsData = ref<StatsData>({
  sources: { current: 0, target: 32, label: '知识源' },
  users: { current: 0, target: 656, label: '用户数量' },
  graphs: { current: 0, target: 328, label: '知识图谱' }
})

const animateNumbers = () => {
  Object.keys(statsData.value).forEach((key) => {
    const item = statsData.value[key as keyof StatsData]
    const duration = 2000
    const start = 0
    const end = item.target
    const increment = (end - start) / (duration / 16)
    
    let current = start
    const animate = () => {
      current += increment
      if (current < end) {
        item.current = Math.floor(current)
        requestAnimationFrame(animate)
      } else {
        item.current = end
      }
    }
    animate()
  })
}

const handleCardHover = (e: MouseEvent) => {
  const card = e.currentTarget as HTMLElement
  const rect = card.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  
  const centerX = rect.width / 2
  const centerY = rect.height / 2
  
  const rotateX = (y - centerY) / 10
  const rotateY = (centerX - x) / 10
  
  card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`
  
  const shine = card.querySelector('.card-shine') as HTMLElement
  if (shine) {
    shine.style.opacity = '1'
    shine.style.transform = `translate(${x}px, ${y}px)`
  }
}

const handleCardLeave = (e: MouseEvent) => {
  const card = e.currentTarget as HTMLElement
  card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)'
  
  const shine = card.querySelector('.card-shine') as HTMLElement
  if (shine) {
    shine.style.opacity = '0'
  }
}

const initParticles = () => {
  const particles = document.querySelectorAll('.floating-particle')
  particles.forEach((particle) => {
    const htmlParticle = particle as HTMLElement
    htmlParticle.style.setProperty('--tx', `${Math.random() * 200 - 100}%`)
    htmlParticle.style.setProperty('--ty', `${Math.random() * 200 - 100}%`)
    htmlParticle.style.left = `${Math.random() * 100}%`
    htmlParticle.style.top = `${Math.random() * 100}%`
    htmlParticle.style.animationDelay = `${Math.random() * 20}s`
  })
}

onMounted(() => {
  animateNumbers()
  initParticles()
})

const features = [
  {
    icon: 'fas fa-spider',
    iconClass: 'icon-spider',
    title: '知识建立',
    description: '爬虫抓取网页内容，生成原始内容，形成知识分析，自动生成关键词，并呈现对应的关键内容',
    action: () => router.push('/crawler')
  },
  {
    icon: 'fas fa-network-wired',
    iconClass: 'icon-fusion',
    title: '知识融合',
    description: '智能分析多源数据关联性，自动对齐知识实体，构建完整知识图谱，实现知识的有机整合与互联互通',
    action: () => router.push('/fusion')
  },
  {
    icon: 'fas fa-project-diagram',
    iconClass: 'icon-management',
    title: '知识管理',
    description: '多维度分类整理知识点，可视化展示知识关系网络，支持知识图谱编辑与版本管理，提供协同管理功能',
    action: () => router.push('/management')
  },
  {
    icon: 'fas fa-search',
    iconClass: 'icon-search',
    title: '智能检索',
    description: '基于语义理解的智能搜索，支持多条件组合查询，提供相关知识推荐，快速定位目标知识点并展示知识路径',
    action: () => router.push('/search')
  }
]

const startExplore = () => {
  router.push('/crawler')
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
  animation: fadeIn 1s ease-out;
}

.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.logo-mark {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
  color: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(26, 115, 232, 0.2);
  transition: all 0.3s ease;
}

.logo:hover .logo-mark {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(26, 115, 232, 0.3);
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 600;
  background: linear-gradient(135deg, #1a73e8, #4285f4);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.nav-links a {
  margin-left: 2rem;
  color: #666;
  text-decoration: none;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #1a73e8;
}

.nav-links a i {
  margin-right: 0.5rem;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

.hero-section {
  text-align: center;
  margin-bottom: 6rem;
}

.title {
  font-size: 3.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  animation: fadeInUp 0.8s ease;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 3rem;
  animation: fadeInUp 0.8s ease 0.2s backwards;
}

.stats-row {
  display: flex;
  justify-content: center;
  gap: 4rem;
  margin-bottom: 3rem;
  animation: fadeInUp 0.8s ease 0.4s backwards;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #1a73e8;
  display: inline-block;
  position: relative;
  background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 2px 4px rgba(26, 115, 232, 0.1);
}

.number {
  display: inline-block;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.stat-item:hover .number {
  transform: scale(1.2);
  color: #1557b0;
}

.stat-label {
  color: #666;
  margin-top: 0.5rem;
}

.cta-button {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  animation: fadeInUp 0.8s ease 0.6s backwards;
  box-shadow: 0 4px 15px rgba(26, 115, 232, 0.3);
}

.cta-button:hover {
  background: linear-gradient(135deg, #1557b0 0%, #1a73e8 100%);
  box-shadow: 0 6px 20px rgba(26, 115, 232, 0.4);
  transform: translateY(-2px);
}

.arrow {
  display: inline-block;
  margin-left: 0.5rem;
  transition: transform 0.3s;
}

.cta-button:hover .arrow {
  transform: translateX(5px);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 4rem;
}

.feature-card {
  position: relative;
  overflow: hidden;
  transform-style: preserve-3d;
  transform: perspective(1000px);
  transition: transform 0.3s ease;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  animation: fadeInUp 0.8s ease backwards;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.feature-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  transition: all 0.3s ease;
}

.icon-spider {
  background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
  color: white;
}

.icon-fusion {
  background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%);
  color: white;
}

.icon-management {
  background: linear-gradient(135deg, #7F00FF 0%, #E100FF 100%);
  color: white;
}

.icon-search {
  background: linear-gradient(135deg, #FD746C 0%, #FF9068 100%);
  color: white;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1);
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

.card-shine {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    circle at var(--x, 50%) var(--y, 50%),
    rgba(255, 255, 255, 0.4) 0%,
    rgba(255, 255, 255, 0) 50%
  );
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.background-animation {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.floating-particle {
  position: absolute;
  width: 6px;
  height: 6px;
  background: linear-gradient(135deg, rgba(26, 115, 232, 0.2), rgba(66, 133, 244, 0.2));
  border-radius: 50%;
  animation: float 20s infinite linear;
  box-shadow: 0 0 10px rgba(26, 115, 232, 0.1);
}

@keyframes float {
  0% {
    transform: translate(0, 0);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translate(var(--tx), var(--ty));
    opacity: 0;
  }
}

.floating-particle {
  --tx: random(-100, 100);
  --ty: random(-100, 100);
}

.feature-card:focus,
.cta-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(26, 115, 232, 0.3);
}

@media (max-width: 768px) {
  .stats-row {
    flex-direction: column;
    gap: 2rem;
  }
  
  .title {
    font-size: 2.5rem;
  }
  
  .feature-card {
    transform: none !important; /* 在移动端禁用 3D 效果 */
  }
}

.background-pattern {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/pattern.png');
  opacity: 0.03;
  z-index: -2;
}

.background-gradient {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    linear-gradient(120deg, rgba(96, 108, 136, 0.4) 0%, rgba(63, 76, 119, 0.1) 100%),
    linear-gradient(60deg, rgba(0, 172, 193, 0.1) 0%, rgba(0, 172, 193, 0) 100%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.9) 0%, rgba(245, 247, 250, 0.9) 100%);
  z-index: -1;
}

@keyframes neon {
  0%, 100% {
    filter: drop-shadow(0 0 2px rgba(26, 115, 232, 0.5));
  }
  50% {
    filter: drop-shadow(0 0 5px rgba(26, 115, 232, 0.8));
  }
}

.logo-mark {
  animation: neon 3s ease-in-out infinite;
}
</style>