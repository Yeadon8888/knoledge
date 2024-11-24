<template>
  <div class="chat-container">
    <!-- 左侧对话列表 -->
    <div class="chat-sidebar">
      <div class="new-chat" @click="createNewChat">
        <el-button type="primary" class="new-chat-btn">
          <el-icon><Plus /></el-icon>
          新建对话
        </el-button>
      </div>
      <div class="chat-list">
        <div
          v-for="chat in chatList"
          :key="chat.id"
          class="chat-item"
          :class="{ active: currentChat?.id === chat.id }"
          @click="selectChat(chat)"
        >
          <el-icon><ChatDotRound /></el-icon>
          <span class="chat-title">{{ chat.title }}</span>
        </div>
      </div>
    </div>

    <!-- 右侧聊天窗口 -->
    <div class="chat-main">
      <div class="chat-header">
        <h2>{{ currentChat?.title || '新对话' }}</h2>
      </div>
      
      <div class="chat-messages" ref="messagesContainer">
        <div
          v-for="(message, index) in currentChat?.messages"
          :key="index"
          class="message"
          :class="message.role"
        >
          <div class="message-content">
            <div v-if="message.role === 'assistant'" class="avatar">
              <img src="/ai-avatar.png" alt="AI">
            </div>
            <div v-else class="avatar">
              <img src="/user-avatar.png" alt="User">
            </div>
            <div class="message-text">
              <template v-if="message.role === 'assistant' && message.isTyping">
                <span class="typing-animation">
                  <span>.</span><span>.</span><span>.</span>
                </span>
              </template>
              <template v-else>
                {{ message.content }}
              </template>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input">
        <el-input
          v-model="userInput"
          type="textarea"
          :rows="3"
          placeholder="输入您的问题..."
          resize="none"
          @keydown.enter.exact.prevent="sendMessage"
        />
        <el-button
          type="primary"
          :disabled="!userInput.trim()"
          @click="sendMessage"
        >
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted } from 'vue'
import { Plus, ChatDotRound } from '@element-plus/icons-vue'

interface Message {
  role: 'user' | 'assistant'
  content: string
  isTyping?: boolean
}

interface Chat {
  id: number
  title: string
  messages: Message[]
}

const chatList = ref<Chat[]>([])
const currentChatId = ref<number | null>(null)
const userInput = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

// 模拟的AI回复
const aiResponses = [
  "根据您的问题，我建议您可以查看以下相关文档...",
  "这个问题涉及到几个方面，让我为您详细解答...",
  "我找到了一些相关的知识点，可能对您有帮助...",
  "这是一个很好的问题，让我从以下几个角度为您分析...",
]

const currentChat = computed(() => 
  chatList.value.find(chat => chat.id === currentChatId.value)
)

const createNewChat = () => {
  const newChat: Chat = {
    id: Date.now(),
    title: `新对话 ${chatList.value.length + 1}`,
    messages: []
  }
  chatList.value.push(newChat)
  currentChatId.value = newChat.id
}

const selectChat = (chat: Chat) => {
  currentChatId.value = chat.id
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const simulateTyping = async (response: string) => {
  const message: Message = {
    role: 'assistant',
    content: response,
    isTyping: true
  }
  currentChat.value?.messages.push(message)
  await scrollToBottom()
  
  // 模拟打字效果
  await new Promise(resolve => setTimeout(resolve, 1500))
  message.isTyping = false
  await scrollToBottom()
}

const sendMessage = async () => {
  if (!userInput.value.trim()) return
  
  if (!currentChat.value) {
    createNewChat()
  }
  
  // 添加用户消息
  currentChat.value?.messages.push({
    role: 'user',
    content: userInput.value
  })
  
  userInput.value = ''
  await scrollToBottom()
  
  // 模拟AI回复
  const randomResponse = aiResponses[Math.floor(Math.random() * aiResponses.length)]
  await simulateTyping(randomResponse)
}

// 创建初始对话
onMounted(() => {
  createNewChat()
})
</script>

<style scoped>
.chat-container {
  display: flex;
  height: calc(100vh - 60px);
  background: #fff;
}

.chat-sidebar {
  width: 260px;
  border-right: 1px solid #e6e6e6;
  display: flex;
  flex-direction: column;
}

.new-chat {
  padding: 16px;
  border-bottom: 1px solid #e6e6e6;
}

.new-chat-btn {
  width: 100%;
}

.chat-list {
  flex: 1;
  overflow-y: auto;
}

.chat-item {
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.chat-item:hover {
  background-color: #f5f7fa;
}

.chat-item.active {
  background-color: #ecf5ff;
}

.chat-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-header {
  padding: 16px;
  border-bottom: 1px solid #e6e6e6;
}

.chat-header h2 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.message {
  margin-bottom: 24px;
}

.message-content {
  display: flex;
  gap: 12px;
  max-width: 80%;
}

.message.user .message-content {
  margin-left: auto;
  flex-direction: row-reverse;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.message-text {
  padding: 12px 16px;
  border-radius: 12px;
  background: #f4f6f8;
  font-size: 14px;
  line-height: 1.5;
}

.message.assistant .message-text {
  background: #ecf5ff;
}

.message.user .message-text {
  background: #95d475;
  color: white;
}

.typing-animation {
  display: inline-flex;
  gap: 4px;
}

.typing-animation span {
  animation: typing 1s infinite;
  display: inline-block;
}

.typing-animation span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-animation span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #e6e6e6;
  display: flex;
  gap: 12px;
}

.chat-input :deep(.el-textarea__inner) {
  resize: none;
  border-radius: 8px;
}

.chat-input .el-button {
  align-self: flex-end;
}
</style>
