<template>
  <div class="home-page">
    <Hero />
  </div>
</template>

<script setup lang="ts">
import Hero from '../components/Hero.vue'
</script>

<style scoped>
.home-page {
  min-height: calc(100vh - 60px); /* 减去导航栏高度 */
}
</style> 