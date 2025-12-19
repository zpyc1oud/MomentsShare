<template>
  <PageLayout title="消息" :show-back="false">
    <template #nav-right>
      <button class="nav-btn" @click="$router.push('/add-friend')">
        <span v-if="pendingCount" class="badge">{{ pendingCount }}</span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
          <circle cx="8.5" cy="7" r="4"/>
          <path d="M20 8v6M23 11h-6"/>
        </svg>
      </button>
    </template>
    
    <div class="messages-page">
      <!-- 快捷入口 -->
      <div class="quick-entries">
        <div class="entry-item" @click="$router.push('/friends')">
          <div class="entry-icon">👥</div>
          <span class="entry-label">通讯录</span>
        </div>
        <div class="entry-item" @click="$router.push('/friend-requests')">
          <div class="entry-icon">
            ✉️
            <span v-if="pendingCount" class="entry-badge">{{ pendingCount }}</span>
          </div>
          <span class="entry-label">好友申请</span>
        </div>
      </div>
      
      <!-- 消息列表（占位） -->
      <div class="message-list">
        <div class="empty-state">
          <span class="empty-state__icon">💬</span>
          <h3 class="empty-state__title">暂无消息</h3>
          <p class="empty-state__desc">和好友互动后，消息会显示在这里</p>
        </div>
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PageLayout from '@/components/layout/PageLayout.vue'
import { friendsApi } from '@/api/friends'

const pendingCount = ref(0)

const fetchPendingCount = async () => {
  try {
    const response = await friendsApi.getPendingRequests()
    pendingCount.value = response.results ? response.results.length : response.length
  } catch (error) {
    console.error('Fetch pending count error:', error)
  }
}

onMounted(() => {
  fetchPendingCount()
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
  
  svg {
    width: 22px;
    height: 22px;
  }
  
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
  backdrop-filter: blur(10px);
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
  }
}

.entry-label {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.message-list {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

