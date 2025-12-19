<template>
  <PageLayout title="好友申请" :show-back="true" :show-tabbar="false">
    <div class="requests-page">
      <div v-if="loading" class="loading-container">
        <Loading text="加载中..." />
      </div>
      
      <template v-else>
        <div v-if="requests.length > 0" class="request-list">
          <div 
            v-for="request in requests" 
            :key="request.id"
            class="request-item"
          >
            <img :src="request.from_user?.avatar || '/default-avatar.png'" class="avatar" />
            <div class="request-info">
              <span class="request-name">{{ request.from_user?.nickname }}</span>
              <span class="request-time">{{ formatTime(request.created_at) }}</span>
            </div>
            <div class="request-actions">
              <button 
                class="btn btn--primary btn--small"
                @click="handleRespond(request.id, 'accept')"
                :disabled="responding === request.id"
              >
                同意
              </button>
              <button 
                class="btn btn--secondary btn--small"
                @click="handleRespond(request.id, 'reject')"
                :disabled="responding === request.id"
              >
                拒绝
              </button>
            </div>
          </div>
        </div>
        
        <div v-else class="empty-state">
      <van-icon name="envelop-o" class="empty-state__icon" />
      <h3 class="empty-state__title">暂无申请</h3>
      <p class="empty-state__desc">有新的好友申请时会显示在这里</p>
    </div>
      </template>
    </div>
  </PageLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'
import PageLayout from '@/components/layout/PageLayout.vue'
import Loading from '@/components/common/Loading.vue'
import { friendsApi } from '@/api/friends'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

const requests = ref([])
const loading = ref(true)
const responding = ref(null)

const fetchRequests = async () => {
  try {
    const response = await friendsApi.getPendingRequests()
    requests.value = response.results || response
  } catch (error) {
    console.error('Fetch requests error:', error)
  } finally {
    loading.value = false
  }
}

const handleRespond = async (requestId, action) => {
  responding.value = requestId
  
  try {
    await friendsApi.respondRequest(requestId, action)
    // 移除已处理的申请
    requests.value = requests.value.filter(r => r.id !== requestId)
  } catch (error) {
    console.error('Respond error:', error)
  } finally {
    responding.value = null
  }
}

const formatTime = (time) => {
  return dayjs(time).fromNow()
}

onMounted(() => {
  fetchRequests()
})
</script>

<style lang="scss" scoped>
.requests-page {
  height: 100%;
  padding: $spacing-md;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: $spacing-xl;
}

.request-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.request-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-md;
  background: $glass-bg;
  backdrop-filter: $glass-blur;
  border: $glass-border-light;
  border-radius: $radius-lg;
  box-shadow: $shadow-sm;
}

.request-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.request-name {
  font-size: $font-size-base;
  font-weight: $font-weight-medium;
  color: $text-primary;
}

.request-time {
  font-size: $font-size-xs;
  color: $text-muted;
}

.request-actions {
  display: flex;
  gap: $spacing-xs;
}
</style>

