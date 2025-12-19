<template>
  <PageLayout title="通讯录" :show-back="true" :show-tabbar="false">
    <div class="friends-page">
      <div v-if="loading" class="loading-container">
        <Loading text="加载中..." />
      </div>
      
      <template v-else>
        <div v-if="friends.length > 0" class="friend-list">
          <div 
            v-for="friend in friends" 
            :key="friend.id"
            class="friend-item"
            @click="goToProfile(friend.id)"
          >
            <img :src="friend.avatar || '/default-avatar.png'" class="avatar" />
            <div class="friend-info">
              <span class="friend-name">{{ friend.nickname }}</span>
              <span class="friend-username">@{{ friend.username }}</span>
            </div>
            <van-icon name="arrow" class="arrow-icon" />
          </div>
        </div>
        
        <div v-else class="empty-state">
          <van-icon name="friends-o" class="empty-state__icon" />
          <h3 class="empty-state__title">暂无好友</h3>
          <p class="empty-state__desc">快去添加好友开始社交吧</p>
        </div>
      </template>
    </div>
  </PageLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PageLayout from '@/components/layout/PageLayout.vue'
import Loading from '@/components/common/Loading.vue'
import { friendsApi } from '@/api/friends'

const router = useRouter()

const friends = ref([])
const loading = ref(true)

const fetchFriends = async () => {
  try {
    const response = await friendsApi.getFriendList()
    friends.value = response.results || response
  } catch (error) {
    console.error('Fetch friends error:', error)
  } finally {
    loading.value = false
  }
}

const goToProfile = (id) => {
  router.push(`/user/${id}`)
}

onMounted(() => {
  fetchFriends()
})
</script>

<style lang="scss" scoped>
.friends-page {
  height: 100%;
  padding: $spacing-md;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: $spacing-xl;
}

.friend-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.friend-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-md;
  background: $glass-bg;
  backdrop-filter: $glass-blur;
  border: $glass-border-light;
  border-radius: $radius-lg;
  cursor: pointer;
  transition: all $transition-fast;
  box-shadow: $shadow-sm;
  
  &:hover {
    background: $glass-bg-heavy;
    transform: translateX(4px);
  }
}

.friend-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.friend-name {
  font-size: $font-size-base;
  font-weight: $font-weight-medium;
  color: $text-primary;
}

.friend-username {
  font-size: $font-size-sm;
  color: $text-muted;
}

.arrow-icon {
  font-size: 20px;
  color: $text-muted;
}
</style>

