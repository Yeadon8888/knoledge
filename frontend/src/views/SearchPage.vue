<template>
  <div class="chat-container">
    <el-card class="chat-card">
      <div class="chat-header">
        <h2>智能知识助手</h2>
        <p>我是您的知识管理助手，请告诉我您想了解什么？</p>
      </div>

      <div class="gradio-container">
        <iframe
          src="http://localhost:7860"
          width="100%"
          height="600px"
          frameborder="0"
          style="border-radius: 8px;"
          allow="clipboard-read; clipboard-write"
        ></iframe>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" 
          :class="['message', message.role === 'user' ? 'user-message' : 'assistant-message']">
          <div class="message-avatar">
            {{ message.role === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="message-content" v-html="formatMessage(message.content)"></div>
        </div>
      </div>

      <div class="chat-input">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="3"
          placeholder="请输入您的问题..."
          @keyup.enter.exact.prevent="handleSend"
          :disabled="loading"
        />
        <div class="button-group">
          <el-button 
            type="primary" 
            :loading="loading"
            @click="handleSend"
            class="send-button"
          >
            发送
          </el-button>
          <el-button 
            @click="clearChat"
            class="clear-button"
          >
            清除对话
          </el-button>
        </div>
      </div>

      <div class="example-questions">
        <h4>示例问题：</h4>
        <el-button
          v-for="(question, index) in exampleQuestions"
          :key="index"
          link
          type="primary"
          @click="useExample(question)"
        >
          {{ question }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import * as DOMPurify from 'dompurify'
import { marked } from 'marked'

const inputMessage = ref('')
const loading = ref(false)
const messages = ref<Array<{role: 'user' | 'assistant', content: string}>>([])
const messagesContainer = ref<HTMLElement | null>(null)

const exampleQuestions = [
  "什么是机器学习？",
  "Python和Java的主要区别是什么？",
  "如何提高编程效率？"
]

const formatMessage = (content: string) => {
  return DOMPurify.sanitize(marked(content))
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const handleSend = async () => {
  if (!inputMessage.value.trim()) {
    ElMessage.warning('请输入问题')
    return
  }

  const userMessage = inputMessage.value
  messages.value.push({
    role: 'user',
    content: userMessage
  })
  
  inputMessage.value = ''
  loading.value = true
  
  try {
    const response = await axios.post('http://localhost:8001/search', {
      query: userMessage
    })
    
    messages.value.push({
      role: 'assistant',
      content: response.data.result
    })
    
    await scrollToBottom()
  } catch (error) {
    ElMessage.error('对话失败，请稍后重试')
    console.error('Chat error:', error)
  } finally {
    loading.value = false
  }
}

const clearChat = () => {
  messages.value = []
}

const useExample = (question) => {
  inputMessage.value = question
}

onMounted(() => {
  // 添加欢迎消息
  messages.value.push({
    role: 'assistant',
    content: '你好！我是你的知识管理助手。我可以帮你解答问题，提供知识支持。请问有什么我可以帮你的吗？'
  })
})
</script>

<style scoped>
.chat-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
  height: calc(100vh - 120px);
}

.chat-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  height: 100%;
  overflow: hidden;
}

.chat-header {
  text-align: center;
  margin-bottom: 20px;
  padding: 10px;
}

.chat-header h2 {
  color: #409EFF;
  margin-bottom: 10px;
}

.chat-header p {
  color: #666;
  font-size: 14px;
}

.gradio-container {
  padding: 0 20px 20px 20px;
  height: calc(100% - 100px);
}

.gradio-container iframe {
  height: 100%;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.message {
  display: flex;
  margin-bottom: 20px;
  align-items: flex-start;
}

.message-avatar {
  font-size: 24px;
  margin-right: 12px;
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.message-content {
  background: white;
  padding: 12px 16px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  max-width: 80%;
  line-height: 1.5;
}

.user-message {
  flex-direction: row-reverse;
}

.user-message .message-avatar {
  margin-right: 0;
  margin-left: 12px;
}

.user-message .message-content {
  background: #409EFF;
  color: white;
}

.chat-input {
  padding: 20px;
  background: white;
  border-radius: 8px;
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.send-button {
  flex: 2;
}

.clear-button {
  flex: 1;
}

.example-questions {
  padding: 10px;
  border-top: 1px solid #eee;
}

.example-questions h4 {
  margin-bottom: 10px;
  color: #666;
}

:deep(.el-button--link) {
  margin-right: 15px;
  font-size: 13px;
}

:deep(.markdown-body) {
  background: transparent;
}

:deep(.user-message .markdown-body) {
  color: white;
}

:deep(.el-textarea__inner) {
  resize: none;
}

:deep(.el-card__body) {
  height: 100%;
  padding: 20px;
}
</style>
