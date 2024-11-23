<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import WebCrawler from './components/WebCrawler.vue'

const route = useRoute()
const activeMenu = ref(route.path)
</script>

<template>
  <div class="app-container">
    <el-menu
      :default-active="activeMenu"
      mode="horizontal"
      router
      class="nav-menu"
    >
      <el-menu-item index="/">首页</el-menu-item>
      <el-menu-item index="/crawler">网页分析</el-menu-item>
      <el-menu-item index="/fusion">内容融合</el-menu-item>
    </el-menu>
    
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 0;
  padding: 0;
}

body {
  margin: 0;
  padding: 0;
}

.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.nav-menu {
  padding: 0 20px;
  background: transparent;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

:root {
  --el-menu-hover-bg-color: rgba(255, 255, 255, 0.1);
}

.el-menu--horizontal > .el-menu-item.is-active {
  border-bottom: 2px solid var(--el-menu-active-color);
  background-color: rgba(255, 255, 255, 0.1);
}

.el-menu--horizontal > .el-menu-item:not(.is-disabled):hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>
