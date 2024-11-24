<template>
  <div class="fusion-container">
    <el-card class="fusion-card">
      <template #header>
        <div class="card-header">
          <h2>内容融合</h2>
        </div>
      </template>
      
      <div class="json-inputs">
        <el-card v-for="(input, index) in jsonInputs" :key="index" class="json-input-card">
          <template #header>
            <div class="input-header">
              <h3>JSON Input {{ index + 1 }}</h3>
              <el-button
                type="danger"
                circle
                @click="removeInput(index)"
                v-if="jsonInputs.length > 1"
                :icon="Delete"
              />
            </div>
          </template>
          
          <el-input
            v-model="input.content"
            type="textarea"
            :rows="8"
            :status="input.error ? 'error' : ''"
            placeholder="请输入JSON格式的知识内容..."
            @input="validateJson(index)"
          />
          <div class="error-message" v-if="input.error">{{ input.error }}</div>
        </el-card>
      </div>

      <div class="action-buttons">
        <el-button type="success" @click="addNewInput" :icon="Plus">
          添加新的JSON输入
        </el-button>
        
        <el-button 
          type="primary" 
          @click="performFusion" 
          :disabled="hasErrors || loading"
          :loading="loading"
          :icon="Merge"
        >
          AI融合
        </el-button>
      </div>

      <el-collapse-transition>
        <div v-if="fusionResult" class="result-section">
          <el-divider>合并结果</el-divider>
          <el-card class="result-card">
            <pre class="result-content">{{ fusionResult }}</pre>
          </el-card>
        </div>
      </el-collapse-transition>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Delete, Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const Merge = 'Merge'

interface JsonInput {
  content: string
  error: string | null
}

const jsonInputs = ref<JsonInput[]>([
  { content: '', error: null }
])

const fusionResult = ref('')
const loading = ref(false)

const hasErrors = computed(() => {
  return jsonInputs.value.some(input => input.error !== null || !input.content.trim())
})

const addNewInput = () => {
  jsonInputs.value.push({ content: '', error: null })
}

const removeInput = (index: number) => {
  jsonInputs.value.splice(index, 1)
}

const validateJson = (index: number) => {
  const input = jsonInputs.value[index]
  if (!input.content.trim()) {
    input.error = null
    return
  }
  
  try {
    JSON.parse(input.content)
    input.error = null
  } catch (e) {
    input.error = '无效的JSON格式'
  }
}

const performFusion = async () => {
  if (hasErrors.value) {
    ElMessage.warning('请确保所有输入都是有效的JSON格式')
    return
  }

  if (jsonInputs.value.some(input => !input.content.trim())) {
    ElMessage.warning('请确保所有输入框都不为空')
    return
  }

  loading.value = true
  try {
    // 解析所有JSON输入
    const validInputs = jsonInputs.value
      .filter(input => input.content.trim())
      .map(input => {
        try {
          const parsed = JSON.parse(input.content)
          // 确保解析后的内容是对象类型
          if (typeof parsed !== 'object' || Array.isArray(parsed) || parsed === null) {
            throw new Error('输入必须是JSON对象格式')
          }
          return parsed
        } catch (e) {
          throw new Error(`JSON解析错误: ${e.message}`)
        }
      })

    if (validInputs.length === 0) {
      throw new Error('没有有效的JSON输入')
    }

    // 调用后端API进行AI融合
    const response = await axios.post('http://localhost:8001/merge', {
      contents: validInputs
    })
    
    fusionResult.value = JSON.stringify(response.data.result, null, 2)
    ElMessage.success('内容融合成功')
  } catch (error) {
    console.error('Fusion error:', error)
    ElMessage.error('融合失败：' + (error as Error).message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.fusion-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.fusion-card {
  background: rgba(255, 255, 255, 0.9);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  color: var(--el-text-color-primary);
}

.json-inputs {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.json-input-card {
  margin-bottom: 16px;
}

.input-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.input-header h3 {
  margin: 0;
  color: var(--el-text-color-primary);
}

.error-message {
  color: var(--el-color-danger);
  margin-top: 8px;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin: 24px 0;
}

.result-section {
  margin-top: 24px;
}

.result-card {
  background: var(--el-color-info-light-9);
}

.result-content {
  margin: 0;
  font-family: monospace;
  font-size: 14px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

:deep(.el-card__header) {
  padding: 12px 20px;
}

:deep(.el-textarea__inner) {
  font-family: monospace;
  font-size: 14px;
}
</style>
