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
import axios from 'axios'

// 声明全局G6变量
declare const G6: any

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
      // 更新数据
      graph.data(mindmapData)
      
      // 应用布局
      graph.updateLayout({
        type: 'compactBox',
        direction: 'LR',
        getId: function getId(d: any) {
          return d.id;
        },
        getHeight: () => 60,
        getWidth: () => 160,
        getVGap: () => 80,
        getHGap: () => 200,
      })
      
      // 渲染并适应视图
      graph.render()
      graph.fitView()
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
  if (!container.value || !G6) return
  
  const width = container.value.offsetWidth || 800
  const height = container.value.offsetHeight || 600

  // 注册自定义节点
  G6.registerNode('knowledge-node', {
    draw(cfg: any, group: any) {
      const { label, style = {} } = cfg
      const keyShape = group.addShape('rect', {
        attrs: {
          x: -75,
          y: -25,
          width: 150,
          height: 50,
          radius: 8,
          fill: style.fill || '#91d5ff',
          stroke: style.stroke || '#69c0ff',
          lineWidth: 2,
          cursor: 'pointer',
        },
        name: 'rect-shape',
      });

      group.addShape('text', {
        attrs: {
          text: label,
          x: 0,
          y: 0,
          textAlign: 'center',
          textBaseline: 'middle',
          fill: '#333',
          fontSize: 14,
          fontWeight: 500,
          cursor: 'pointer',
        },
        name: 'text-shape',
      });

      return keyShape;
    },
  });
  
  graph = new G6.Graph({
    container: container.value,
    width,
    height,
    modes: {
      default: ['drag-canvas', 'zoom-canvas', 'drag-node']
    },
    layout: {
      type: 'compactBox',
      direction: 'LR',
      getId: function getId(d: any) {
        return d.id;
      },
      getHeight: () => 60,
      getWidth: () => 160,
      getVGap: () => 80,
      getHGap: () => 200,
    },
    defaultNode: {
      type: 'knowledge-node',
    },
    defaultEdge: {
      type: 'cubic-horizontal',
      style: {
        stroke: '#A3B1BF',
        lineWidth: 2,
        endArrow: {
          path: 'M 0,0 L 8,4 L 8,-4 Z',
          fill: '#A3B1BF',
        },
      }
    },
    fitView: true,
    animate: true,
  })
}

// 处理窗口大小变化
const handleResize = () => {
  if (graph && container.value) {
    const width = container.value.offsetWidth || 800
    const height = container.value.offsetHeight || 600
    graph.changeSize(width, height)
    graph.fitView()
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
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 20px;
  background-color: #f5f7fa;
}

.control-panel {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.button-group {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

#mindmap-container {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  overflow: hidden;
}
</style>
