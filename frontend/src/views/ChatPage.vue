<template>
  <div class="chat-container">
    <div class="chat-header">
      <h1>🤖 智能知识助手</h1>
      <p>基于DeepSeek R1的智能知识管理助手，为您提供专业的知识管理服务</p>
    </div>

    <div class="chat-messages" ref="messagesContainer">
      <div v-for="(message, index) in messages" :key="index" 
           :class="['message', message.role === 'user' ? 'user-message' : 'assistant-message']">
        <div class="message-content">
          <div class="avatar">
            {{ message.role === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="text">{{ message.content }}</div>
        </div>
      </div>
      <div v-if="loading" class="message assistant-message">
        <div class="message-content">
          <div class="avatar">🤖</div>
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <div class="input-container">
        <textarea
          v-model="inputMessage"
          @keydown.enter.prevent="sendMessage"
          placeholder="请输入您的问题..."
          :disabled="loading"
          rows="1"
          ref="inputTextarea"
        ></textarea>
        <button @click="sendMessage" :disabled="loading || !inputMessage.trim()">
          发送
        </button>
      </div>
      <div class="example-questions">
        <div class="examples-title">💡 示例问题：</div>
        <div class="examples-grid">
          <button
            v-for="(question, index) in exampleQuestions"
            :key="index"
            @click="useExample(question)"
            :disabled="loading"
          >
            {{ question }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'

const messages = ref<Array<{role: string, content: string}>>([
  {
    role: 'assistant',
    content: '你好！我是基于DeepSeek R1的智能知识助手。请问有什么我可以帮你的吗？'
  }
])
const inputMessage = ref('')
const loading = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)
const inputTextarea = ref<HTMLTextAreaElement | null>(null)

const exampleQuestions = [
  '如何有效地组织和管理我的知识？',
  '请推荐一些好用的知识管理工具',
  '如何建立个人知识体系？',
  '如何提高学习效率？',
  '如何做好知识的分类和标签管理？'
]

async function sendMessage() {
  const message = inputMessage.value.trim()
  if (!message || loading.value) return

  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: message
  })
  
  inputMessage.value = ''
  loading.value = true

  try {
    // 发送请求到后端
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    })

    if (!response.ok) {
      throw new Error('网络请求失败')
    }

    const data = await response.json()
    
    // 添加助手回复
    messages.value.push({
      role: 'assistant',
      content: data.response
    })
  } catch (error) {
    messages.value.push({
      role: 'assistant',
      content: '抱歉，发生了一些错误。请稍后再试。'
    })
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
  }
}

function useExample(question: string) {
  inputMessage.value = question
  sendMessage()
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

onMounted(() => {
  if (inputTextarea.value) {
    inputTextarea.value.focus()
  }
})
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f7fa;
  padding: 2rem;
}

.chat-header {
  text-align: center;
  margin-bottom: 2rem;
}

.chat-header h1 {
  font-size: 2rem;
  color: #1a237e;
  margin-bottom: 0.5rem;
}

.chat-header p {
  color: #666;
  font-size: 1rem;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.message {
  margin-bottom: 1rem;
}

.message-content {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
}

.user-message .message-content {
  background-color: #e3f2fd;
}

.assistant-message .message-content {
  background-color: #f5f5f5;
}

.avatar {
  font-size: 1.5rem;
  min-width: 2rem;
  text-align: center;
}

.text {
  flex: 1;
  line-height: 1.5;
  white-space: pre-wrap;
}

.chat-input {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.input-container {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

textarea {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  resize: none;
  font-family: inherit;
  font-size: 1rem;
  line-height: 1.5;
  transition: border-color 0.3s;
}

textarea:focus {
  outline: none;
  border-color: #1a237e;
}

button {
  padding: 0.8rem 1.5rem;
  background: #1a237e;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

button:hover:not(:disabled) {
  background: #283593;
  transform: translateY(-1px);
}

button:disabled {
  background: #9e9e9e;
  cursor: not-allowed;
}

.example-questions {
  margin-top: 1.5rem;
}

.examples-title {
  font-weight: 600;
  margin-bottom: 0.8rem;
  color: #666;
}

.examples-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.8rem;
}

.examples-grid button {
  background: #f5f5f5;
  color: #333;
  padding: 0.8rem;
  font-size: 0.9rem;
  text-align: left;
}

.examples-grid button:hover:not(:disabled) {
  background: #e0e0e0;
}

.typing-indicator {
  display: flex;
  gap: 0.3rem;
  padding: 0.5rem 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #1a237e;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

@media (max-width: 768px) {
  .chat-container {
    padding: 1rem;
  }
  
  .examples-grid {
    grid-template-columns: 1fr;
  }
}
</style> 