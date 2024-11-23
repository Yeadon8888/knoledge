<template>
  <div class="home">
    <h1>Welcome to Vue3 + FastAPI Demo</h1>
    <div class="status-check">
      <p>Backend Status: {{ backendStatus }}</p>
      <button @click="checkBackendStatus">Check Backend Status</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'Home',
  setup() {
    const backendStatus = ref('Not checked')

    const checkBackendStatus = async () => {
      try {
        const response = await axios.get('http://localhost:8001/health')
        backendStatus.value = response.data.status
      } catch (error) {
        backendStatus.value = 'Error connecting to backend'
      }
    }

    return {
      backendStatus,
      checkBackendStatus
    }
  }
})
</script>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.status-check {
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
