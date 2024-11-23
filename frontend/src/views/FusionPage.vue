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
          :disabled="hasErrors"
          :icon="Merge"
        >
          合并内容
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

const Merge = 'Merge'

interface JsonInput {
  content: string
  error: string | null
}

const jsonInputs = ref<JsonInput[]>([
  { content: '', error: null }
])

const fusionResult = ref('')

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

const performFusion = () => {
  if (jsonInputs.value.some(input => !input.content.trim())) {
    ElMessage.warning('请确保所有输入框都不为空')
    return
  }

  try {
    // 解析所有JSON输入
    const parsedInputs = jsonInputs.value
      .map(input => JSON.parse(input.content))
      .filter(json => json) // 过滤掉空值

    // 合并逻辑：如果有重复的内容，保留第一个出现的
    const merged = parsedInputs.reduce((result, current) => {
      const newItems = Array.isArray(current) ? current : [current]
      
      newItems.forEach(item => {
        const itemStr = JSON.stringify(item)
        if (!result.some(existing => JSON.stringify(existing) === itemStr)) {
          result.push(item)
        }
      })
      
      return result
    }, [] as any[])

    fusionResult.value = JSON.stringify(merged, null, 2)
    ElMessage.success('内容合并成功')
  } catch (e) {
    console.error('Fusion error:', e)
    ElMessage.error('合并过程中发生错误，请检查输入的JSON格式是否正确')
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
