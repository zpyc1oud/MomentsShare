<template>
  <PageLayout :title="chatTitle" :show-back="true" :show-tabbar="false">
    <div class="chat-page">
      <!-- 消息列表 -->
      <div class="message-list" ref="messageListRef">
        <div v-if="loading" class="loading-container">
          <Loading text="加载中..." />
        </div>
        
        <template v-else>
          <div v-if="messages.length === 0" class="empty-state">
            <van-icon name="chat-o" class="empty-state__icon" />
            <p class="empty-state__desc">暂无消息，发送第一条消息吧</p>
          </div>
          
          <div
            v-for="msg in messages"
            :key="msg.id"
            class="message-item"
            :class="{ 'message-item--self': isSelfMessage(msg) }"
            :style="{ alignSelf: isSelfMessage(msg) ? 'flex-end' : 'flex-start' }"
          >
            <img
              :src="normalizeAvatar(msg.sender.avatar)"
              class="message-avatar"
            />
            <div class="message-bubble">
              <div class="message-content">{{ msg.content }}</div>
              <div class="message-time">{{ formatTime(msg.created_at) }}</div>
            </div>
          </div>
        </template>
      </div>
      
      <!-- 输入框 -->
      <div class="input-area">
        <van-field
          v-model="inputText"
          type="textarea"
          rows="1"
          autosize
          placeholder="输入消息..."
          class="message-input"
          @keydown.enter.exact.prevent="sendMessage"
        />
        <button
          class="send-btn"
          :disabled="!inputText.trim() || sending"
          @click="sendMessage"
        >
          <van-icon name="guide-o" />
        </button>
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { showToast } from 'vant'
import PageLayout from '@/components/layout/PageLayout.vue'
import Loading from '@/components/common/Loading.vue'
import { messagesApi } from '@/api/messages'
import { usersApi } from '@/api/users'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()

const userId = computed(() => parseInt(route.params.userId))
const currentUserId = computed(() => authStore.user?.id)
const otherUser = ref(null)
const messages = ref([])
const loading = ref(true)
const sending = ref(false)
const inputText = ref('')
const messageListRef = ref(null)

const chatTitle = computed(() => otherUser.value?.nickname || '私信')

// 判断消息是否来自当前用户
const isSelfMessage = (msg) => {
  console.log('Checking message:', msg.sender?.id, 'vs current:', currentUserId.value)
  if (!currentUserId.value || !msg?.sender?.id) return false
  return Number(msg.sender.id) === Number(currentUserId.value)
}

const fetchOtherUser = async () => {
  try {
    const response = await usersApi.getUserProfile(userId.value)
    otherUser.value = response
  } catch (error) {
    console.error('Fetch user error:', error)
  }
}

const fetchMessages = async () => {
  try {
    const response = await messagesApi.getMessageHistory(userId.value)
    messages.value = response
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Fetch messages error:', error)
  } finally {
    loading.value = false
  }
}

const sendMessage = async () => {
  const content = inputText.value.trim()
  if (!content || sending.value) return

  sending.value = true
  try {
    const newMsg = await messagesApi.sendMessage(userId.value, content)
    messages.value.push(newMsg)
    inputText.value = ''
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Send message error:', error)
    showToast({
      message: error.response?.data?.receiver_id?.[0] || error.response?.data?.detail || '发送失败',
      type: 'fail'
    })
  } finally {
    sending.value = false
  }
}

const scrollToBottom = () => {
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

const normalizeAvatar = (url) => {
  if (!url) return '/media/default_avatar.png'
  
  let finalUrl = url
  if (finalUrl.includes('host.docker.internal')) {
    finalUrl = finalUrl.replace('host.docker.internal', 'localhost')
  }
  
  if (finalUrl.startsWith('http')) return finalUrl
  
  const origin = import.meta.env.VITE_API_ORIGIN || 'http://localhost:8000'
  return `${origin}${finalUrl}`
}

const formatTime = (dateStr) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  // 确保当前用户信息已加载
  if (!authStore.user) {
    await authStore.fetchUserInfo()
  }
  await fetchOtherUser()
  await fetchMessages()
})
</script>

<style lang="scss" scoped>
.chat-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: $bg-base;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: $spacing-md;
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: $spacing-xl;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: $spacing-xl;
  flex: 1;
  
  &__icon {
    font-size: 48px;
    color: $text-muted;
    margin-bottom: $spacing-md;
  }
  
  &__desc {
    font-size: $font-size-sm;
    color: $text-muted;
  }
}

.message-item {
  display: flex;
  align-items: flex-start;
  gap: $spacing-sm;
  max-width: 80%;
  
  &--self {
    align-self: flex-end;
    flex-direction: row-reverse;
    
    .message-bubble {
      background: $pink-primary;
      color: white;
      border-radius: $radius-lg $radius-sm $radius-lg $radius-lg;
    }
    
    .message-time {
      text-align: right;
      color: $text-muted;
    }
  }
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.message-bubble {
  background: white;
  padding: $spacing-sm $spacing-md;
  border-radius: $radius-sm $radius-lg $radius-lg $radius-lg;
  box-shadow: $shadow-sm;
}

.message-content {
  font-size: $font-size-base;
  line-height: 1.5;
  word-break: break-word;
}

.message-time {
  font-size: $font-size-xs;
  color: $text-muted;
  margin-top: $spacing-xs;
}

.input-area {
  display: flex;
  align-items: flex-end;
  gap: $spacing-sm;
  padding: $spacing-md;
  background: white;
  border-top: 1px solid $border-light;
}

.message-input {
  flex: 1;
  background: $bg-base;
  border-radius: $radius-lg;
  
  :deep(.van-field__control) {
    max-height: 100px;
  }
}

.send-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: $pink-primary;
  color: white;
  border-radius: 50%;
  font-size: 20px;
  transition: all $transition-fast;
  
  &:disabled {
    background: $text-muted;
    opacity: 0.5;
  }
  
  &:not(:disabled):hover {
    transform: scale(1.05);
  }
}
</style>
