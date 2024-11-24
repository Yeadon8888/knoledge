<template>
  <div class="mindmap-page">
    <div class="control-panel">
      <el-input
        type="textarea"
        v-model="jsonInput"
        :rows="8"
        placeholder="请输入JSON数据"
        @input="validateJson"
      />
      <div class="button-group">
        <el-button 
          type="primary" 
          @click="generateMindmap"
          :loading="loading"
          :disabled="!isValidJson"
        >
          生成脑图
        </el-button>
      </div>
    </div>
    
    <div id="mindmap-container" ref="container"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElInput, ElButton } from 'element-plus'
import G6 from '@antv/g6'
import axios from 'axios'

// 确保组件名称正确
defineOptions({
  name: 'MindMapPage'
})

const container = ref<HTMLElement | null>(null)
const jsonInput = ref('')
const isValidJson = ref(false)
const loading = ref(false)
let graph: any = null

// 验证JSON输入
const validateJson = () => {
  try {
    if (!jsonInput.value.trim()) {
      isValidJson.value = false
      return
    }
    JSON.parse(jsonInput.value)
    isValidJson.value = true
  } catch (e) {
    isValidJson.value = false
  }
}

// 生成脑图
const generateMindmap = async () => {
  if (!isValidJson.value) {
    ElMessage.warning('请输入有效的JSON数据')
    return
  }

  loading.value = true
  try {
    const jsonData = JSON.parse(jsonInput.value)
    const response = await axios.post('http://localhost:8001/mindmap', {
      json_data: jsonData
    })
    
    const mindmapData = response.data.mindmap_data
    if (graph) {
      graph.data(mindmapData)
      graph.render()
    }
    
    ElMessage.success('脑图生成成功')
  } catch (error) {
    console.error('Generate mindmap error:', error)
    ElMessage.error('生成脑图失败')
  } finally {
    loading.value = false
  }
}

// 初始化G6图表
const initGraph = () => {
  if (!container.value) return
  
  const width = container.value.offsetWidth || 800
  const height = container.value.offsetHeight || 600
  
  graph = new G6.Graph({
    container: container.value,
    width,
    height,
    modes: {
      default: ['drag-canvas', 'zoom-canvas', 'drag-node']
    },
    layout: {
      type: 'mindmap',
      direction: 'H',
      getHeight: () => 40,
      getWidth: () => 100,
      getVGap: () => 20,
      getHGap: () => 100
    },
    defaultNode: {
      type: 'rect',
      style: {
        radius: 5,
        stroke: '#69c0ff',
        fill: '#ffffff',
        lineWidth: 2,
        fillOpacity: 0.9
      }
    },
    defaultEdge: {
      type: 'cubic-horizontal',
      style: {
        stroke: '#A3B1BF',
        lineWidth: 2
      }
    }
  })
}

// 处理窗口大小变化
const handleResize = () => {
  if (graph && container.value) {
    const width = container.value.offsetWidth || 800
    const height = container.value.offsetHeight || 600
    graph.changeSize(width, height)
  }
}

onMounted(() => {
  initGraph()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (graph) {
    graph.destroy()
  }
})
</script>

<style scoped>
.mindmap-page {
  height: calc(100vh - 60px);
  display: flex;
  padding: 20px;
  gap: 20px;
  background-color: #f5f7fa;
}

.control-panel {
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.button-group {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

#mindmap-container {
  flex: 1;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  background: #fff;
  min-height: 500px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
