<template>
  <PageLayout title="" :show-navbar="false">
    <div class="profile-page">
      <!-- 个人信息头部 -->
      <div class="profile-header">
        <div class="profile-bg"></div>
        <div class="profile-info">
          <img :src="user?.avatar || '/default-avatar.png'" class="profile-avatar" />
          <h2 class="profile-name">{{ user?.nickname }}</h2>
          <p class="profile-username">@{{ user?.username }}</p>
        </div>
        <button class="edit-btn" @click="$router.push('/profile/edit')">
          编辑资料
        </button>
      </div>
      
      <!-- 统计信息 -->
      <div class="profile-stats">
        <div class="stat-item">
          <span class="stat-value">{{ stats.moments }}</span>
          <span class="stat-label">动态</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ stats.friends }}</span>
          <span class="stat-label">好友</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ stats.likes }}</span>
          <span class="stat-label">获赞</span>
        </div>
      </div>
      
      <!-- 菜单列表 -->
      <div class="profile-menu">
        <div class="menu-item" @click="$router.push('/friends')">
          <span class="menu-icon">👥</span>
          <span class="menu-label">我的好友</span>
          <svg class="menu-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 18l6-6-6-6"/>
          </svg>
        </div>
        <div class="menu-item" @click="$router.push('/settings')">
          <span class="menu-icon">⚙️</span>
          <span class="menu-label">设置</span>
          <svg class="menu-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 18l6-6-6-6"/>
          </svg>
        </div>
      </div>
      
      <!-- 我的动态 -->
      <div class="my-moments">
        <h3 class="section-title">我的动态</h3>
        <div v-if="moments.length > 0" class="moments-grid">
          <div 
            v-for="moment in moments" 
            :key="moment.id"
            class="moment-thumb"
            @click="$router.push(`/moment/${moment.id}`)"
          >
            <img 
              v-if="moment.type === 'IMAGE' && moment.images?.[0]"
              :src="moment.images[0].image_file" 
              alt=""
            />
            <div v-else class="moment-text">
              {{ moment.content?.slice(0, 20) }}...
            </div>
          </div>
        </div>
        <div v-else class="empty-moments">
          还没有发布动态
        </div>
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import PageLayout from '@/components/layout/PageLayout.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const user = ref(authStore.userInfo)
const stats = reactive({
  moments: 0,
  friends: 0,
  likes: 0
})
const moments = ref([])

onMounted(async () => {
  // 获取用户信息
  const userInfo = await authStore.fetchUserInfo()
  if (userInfo) {
    user.value = userInfo
  }
  
  // TODO: 获取统计数据和动态列表
})
</script>

<style lang="scss" scoped>
.profile-page {
  min-height: 100%;
}

.profile-header {
  position: relative;
  padding: 60px $spacing-lg $spacing-lg;
  text-align: center;
}

.profile-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 120px;
  background: $primary-gradient;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -30px;
    left: 0;
    right: 0;
    height: 60px;
    background: linear-gradient(to bottom, transparent, $bg-dark);
  }
}

.profile-info {
  position: relative;
  z-index: 1;
}

.profile-avatar {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  border: 4px solid $bg-dark;
  object-fit: cover;
  background: $bg-card;
}

.profile-name {
  font-size: $font-size-xl;
  font-weight: $font-weight-bold;
  color: $text-primary;
  margin-top: $spacing-sm;
}

.profile-username {
  font-size: $font-size-sm;
  color: $text-muted;
  margin-top: 4px;
}

.edit-btn {
  position: absolute;
  top: $spacing-md;
  right: $spacing-md;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: $radius-full;
  font-size: $font-size-sm;
  color: $text-primary;
  backdrop-filter: blur(4px);
}

.profile-stats {
  display: flex;
  justify-content: center;
  gap: $spacing-xl;
  padding: $spacing-md 0;
  border-bottom: 1px solid $border-light;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: $font-size-xl;
  font-weight: $font-weight-bold;
  color: $text-primary;
}

.stat-label {
  font-size: $font-size-xs;
  color: $text-muted;
}

.profile-menu {
  padding: $spacing-md;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-md;
  background: $bg-card;
  border-radius: $radius-lg;
  margin-bottom: $spacing-sm;
  cursor: pointer;
  transition: all $transition-fast;
  
  &:hover {
    background: $bg-card-hover;
  }
}

.menu-icon {
  font-size: 22px;
}

.menu-label {
  flex: 1;
  font-size: $font-size-base;
  color: $text-primary;
}

.menu-arrow {
  width: 20px;
  height: 20px;
  color: $text-muted;
}

.my-moments {
  padding: $spacing-md;
}

.section-title {
  font-size: $font-size-base;
  font-weight: $font-weight-semibold;
  color: $text-primary;
  margin-bottom: $spacing-md;
}

.moments-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
}

.moment-thumb {
  aspect-ratio: 1;
  border-radius: $radius-sm;
  overflow: hidden;
  cursor: pointer;
  background: $bg-card;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.moment-text {
  width: 100%;
  height: 100%;
  padding: $spacing-sm;
  font-size: $font-size-xs;
  color: $text-secondary;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.empty-moments {
  text-align: center;
  padding: $spacing-xl;
  color: $text-muted;
  font-size: $font-size-sm;
}
</style>

