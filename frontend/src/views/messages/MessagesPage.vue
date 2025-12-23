<template>
  <PageLayout title="消息" :show-back="false">
    <template #nav-right>
      <button class="nav-btn" @click="$router.push('/add-friend')">
        <van-icon name="friends-o" />
      </button>
    </template>
    
    <div class="messages-page">
      <!-- 快捷入口 -->
      <div class="quick-entries">
        <div class="entry-item" @click="$router.push('/friends')">
          <div class="entry-icon"><van-icon name="friends" /></div>
          <span class="entry-label">通讯录</span>
        </div>
        <div class="entry-item" @click="$router.push('/friend-requests')">
          <div class="entry-icon">
            <van-icon name="envelop-o" />
            <span v-if="pendingCount" class="entry-badge">{{ pendingCount }}</span>
          </div>
          <span class="entry-label">好友申请</span>
        </div>
      </div>
      
      <!-- 会话列表 -->
      <div class="conversation-list">
        <div v-if="loading" class="loading-container">
          <Loading text="加载中..." />
        </div>
        
        <template v-else>
          <div v-if="conversations.length === 0" class="empty-state">
            <van-icon name="chat-o" class="empty-state__icon" />
            <h3 class="empty-state__title">暂无消息</h3>
            <p class="empty-state__desc">和好友互动后，消息会显示在这里</p>
          </div>
          
          <div
            v-for="conv in conversations"
            :key="conv.user.id"
            class="conversation-item"
            @click="goToChat(conv.user.id)"
          >
            <div class="avatar-wrapper">
              <img :src="normalizeAvatar(conv.user.avatar)" class="avatar" />
              <span v-if="conv.unread_count" class="unread-badge">
                {{ conv.unread_count > 99 ? '99+' : conv.unread_count }}
              </span>
            </div>
            <div class="conversation-info">
              <div class="conversation-header">
                <span class="conversation-name">{{ conv.user.nickname }}</span>
                <span class="conversation-time">{{ formatTime(conv.last_message_time) }}</span>
              </div>
              <p class="conversation-preview">{{ conv.last_message }}</p>
            </div>
          </div>
        </template>
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PageLayout from '@/components/layout/PageLayout.vue'
import Loading from '@/components/common/Loading.vue'
import { friendsApi } from '@/api/friends'
import { messagesApi } from '@/api/messages'

const router = useRouter()

const pendingCount = ref(0)
const conversations = ref([])
const loading = ref(true)

const fetchPendingCount = async () => {
  try {
    const response = await friendsApi.getPendingRequests()
    pendingCount.value = response.results ? response.results.length : response.length
  } catch (error) {
    console.error('Fetch pending count error:', error)
  }
}

const fetchConversations = async () => {
  try {
    const response = await messagesApi.getConversations()
    conversations.value = response
  } catch (error) {
    console.error('Fetch conversations error:', error)
  } finally {
    loading.value = false
  }
}

const goToChat = (userId) => {
  router.push(`/chat/${userId}`)
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
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

onMounted(() => {
  fetchPendingCount()
  fetchConversations()
})
</script>

<style lang="scss" scoped>
.messages-page {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.nav-btn {
  position: relative;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  
  .badge {
    position: absolute;
    top: 0;
    right: 0;
    min-width: 16px;
    height: 16px;
    padding: 0 4px;
    background: $error-color;
    border-radius: 8px;
    font-size: 10px;
    line-height: 16px;
    text-align: center;
  }
}

.quick-entries {
  display: flex;
  gap: $spacing-md;
  padding: $spacing-md;
  background: $glass-bg;
  backdrop-filter: $glass-blur;
  border-bottom: $glass-border-light;
}

.entry-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $spacing-xs;
  padding: $spacing-md;
  background: $glass-bg-heavy;
  border: $glass-border-light;
  border-radius: $radius-lg;
  cursor: pointer;
  transition: all $transition-fast;
  box-shadow: $shadow-sm;
  
  &:hover {
    background: rgba(255, 255, 255, 0.8);
    transform: translateY(-2px);
  }
}

.entry-icon {
  position: relative;
  font-size: 28px;
  color: $pink-primary;
  
  .entry-badge {
    position: absolute;
    top: -4px;
    right: -8px;
    min-width: 16px;
    height: 16px;
    padding: 0 4px;
    background: $error-color;
    border-radius: 8px;
    font-size: 10px;
    line-height: 16px;
    text-align: center;
    color: white;
  }
}

.entry-label {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: $spacing-md;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: $spacing-xl;
}

.conversation-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-md;
  background: $glass-bg;
  backdrop-filter: $glass-blur;
  border: $glass-border-light;
  border-radius: $radius-lg;
  margin-bottom: $spacing-sm;
  cursor: pointer;
  transition: all $transition-fast;
  box-shadow: $shadow-sm;

  &:hover {
    background: $glass-bg-heavy;
    transform: translateX(4px);
  }
}

.avatar-wrapper {
  position: relative;
  flex-shrink: 0;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.unread-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  background: $error-color;
  border-radius: 9px;
  font-size: 11px;
  line-height: 18px;
  text-align: center;
  color: white;
  font-weight: bold;
}

.conversation-info {
  flex: 1;
  min-width: 0;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-xs;
}

.conversation-name {
  font-size: $font-size-base;
  font-weight: $font-weight-medium;
  color: $text-primary;
}

.conversation-time {
  font-size: $font-size-xs;
  color: $text-muted;
}

.conversation-preview {
  font-size: $font-size-sm;
  color: $text-secondary;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: $spacing-xl * 2;
  
  &__icon {
    font-size: 48px;
    color: $text-muted;
    margin-bottom: $spacing-md;
  }
  
  &__title {
    font-size: $font-size-lg;
    font-weight: $font-weight-medium;
    color: $text-primary;
    margin-bottom: $spacing-sm;
  }
  
  &__desc {
    font-size: $font-size-sm;
    color: $text-muted;
  }
}
</style>

