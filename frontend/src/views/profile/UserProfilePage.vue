<template>
  <PageLayout title="用户资料" :show-back="true" :show-tabbar="false">
    <div class="user-profile">
      <div v-if="loading" class="loading-container">
        <Loading text="加载中..." />
      </div>
      
      <template v-else-if="user">
        <!-- 用户信息 -->
        <div class="user-header">
          <img :src="user.avatar || '/default-avatar.png'" class="user-avatar" />
          <h2 class="user-name">{{ user.nickname }}</h2>
          <p class="user-username">@{{ user.username }}</p>
          
          <!-- 好友操作按钮 -->
          <button 
            v-if="!isFriend" 
            class="btn btn--primary"
            :disabled="requesting"
            @click="sendFriendRequest"
          >
            {{ requesting ? '发送中...' : '添加好友' }}
          </button>
          <button v-else class="btn btn--secondary" disabled>
            已是好友
          </button>
        </div>
        
        <!-- 用户动态 -->
        <div class="user-moments">
          <h3 class="section-title">TA的动态</h3>
          <div v-if="moments.length > 0" class="moments-list">
            <MomentCard 
              v-for="moment in moments" 
              :key="moment.id"
              :moment="moment"
              @click="$router.push(`/moment/${moment.id}`)"
            />
          </div>
          <div v-else class="empty-moments">
            暂无动态
          </div>
        </div>
      </template>
    </div>
  </PageLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import PageLayout from '@/components/layout/PageLayout.vue'
import Loading from '@/components/common/Loading.vue'
import MomentCard from '@/components/business/MomentCard.vue'
import { friendsApi } from '@/api/friends'

const route = useRoute()

const user = ref(null)
const moments = ref([])
const loading = ref(true)
const isFriend = ref(false)
const requesting = ref(false)

const sendFriendRequest = async () => {
  requesting.value = true
  
  try {
    await friendsApi.sendRequest(route.params.id)
    alert('好友申请已发送')
  } catch (error) {
    const message = error.response?.data?.detail || '发送失败'
    alert(message)
  } finally {
    requesting.value = false
  }
}

onMounted(async () => {
  // TODO: 获取用户信息和动态
  loading.value = false
})
</script>

<style lang="scss" scoped>
.user-profile {
  height: 100%;
  padding: $spacing-md;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: $spacing-xl;
}

.user-header {
  text-align: center;
  padding: $spacing-xl 0;
}

.user-avatar {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: $spacing-md;
}

.user-name {
  font-size: $font-size-xl;
  font-weight: $font-weight-bold;
  color: $text-primary;
}

.user-username {
  font-size: $font-size-sm;
  color: $text-muted;
  margin-bottom: $spacing-md;
}

.user-moments {
  padding-top: $spacing-md;
}

.section-title {
  font-size: $font-size-base;
  font-weight: $font-weight-semibold;
  color: $text-primary;
  margin-bottom: $spacing-md;
}

.moments-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.empty-moments {
  text-align: center;
  padding: $spacing-xl;
  color: $text-muted;
}
</style>

