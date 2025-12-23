<template>
  <PageLayout title="用户资料" :show-back="true" :show-tabbar="false">
    <div class="user-profile">
      <div v-if="loading" class="loading-container">
        <Loading text="加载中..." />
      </div>
      
      <template v-else-if="user">
        <!-- 用户信息 -->
        <div class="user-header">
          <img :src="normalizeAvatar(user?.avatar)" class="user-avatar" />
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
import { showToast } from 'vant'
import PageLayout from '@/components/layout/PageLayout.vue'
import Loading from '@/components/common/Loading.vue'
import MomentCard from '@/components/business/MomentCard.vue'
import { friendsApi } from '@/api/friends'
import { authApi } from '@/api/auth'
import { momentsApi } from '@/api/moments'

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
    showToast({
      message: '好友申请已发送',
      type: 'success'
    })
  } catch (error) {
    const message = error.response?.data?.detail || '发送失败'
    showToast({
      message,
      type: 'fail'
    })
  } finally {
    requesting.value = false
  }
}

// 头像地址兜底
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

onMounted(async () => {
  const userId = route.params.id

  try {
    // 并行获取用户信息和动态
    const [userRes, momentsRes] = await Promise.all([
      authApi.getUserById(userId),
      momentsApi.getUserMoments(userId)
    ])

    user.value = userRes
    moments.value = momentsRes.results || momentsRes
  } catch (error) {
    console.error('加载用户主页失败:', error)
    showToast({
      message: error.response?.data?.detail || '加载用户信息失败',
      type: 'fail'
    })
  } finally {
    loading.value = false
  }
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

