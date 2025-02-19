<template>
  <div class="chat-container">
    <iframe
      src="http://localhost:7860"
      class="chat-frame"
      allow="microphone"
      frameborder="0"
    ></iframe>
  </div>
</template>

<script setup lang="ts">
// 组件逻辑
</script>

<style scoped>
.chat-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.chat-frame {
  flex: 1;
  width: 100%;
  height: 100%;
  border: none;
  background: #fff;
}
</style> 