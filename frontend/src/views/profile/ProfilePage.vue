<template>
  <PageLayout title="" :show-navbar="false">
    <div class="profile-page">
      <!-- 个人信息头部 -->
      <div class="profile-header">
        <!-- 渐变背景 -->
        <div class="profile-bg">
          <div class="profile-bg__blob profile-bg__blob--1"></div>
          <div class="profile-bg__blob profile-bg__blob--2"></div>
        </div>
        
        <div class="profile-info">
          <div class="avatar-container">
            <img :src="normalizeAvatar(user?.avatar)" class="profile-avatar" />
          </div>
          <h2 class="profile-name">{{ user?.nickname }}</h2>
          <p class="profile-username">@{{ user?.username }}</p>
        </div>
        
        <button class="edit-btn" @click="$router.push('/profile/edit')">
          编辑资料
        </button>
      </div>
      
      <!-- 统计信息 - 毛玻璃卡片 -->
      <div class="profile-stats">
        <div class="stat-item">
          <span class="stat-value">{{ stats.moments }}</span>
          <span class="stat-label">动态</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-value">{{ stats.friends }}</span>
          <span class="stat-label">好友</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-value">{{ stats.likes }}</span>
          <span class="stat-label">获赞</span>
        </div>
      </div>
      
      <!-- 菜单列表 -->
      <div class="profile-menu">
        <div class="menu-item" @click="$router.push('/friends')">
          <van-icon name="friends-o" class="menu-icon" />
          <span class="menu-label">我的好友</span>
          <van-icon name="arrow" class="menu-arrow" />
        </div>
        <div class="menu-item" @click="$router.push('/settings')">
          <van-icon name="setting-o" class="menu-icon" />
          <span class="menu-label">设置</span>
          <van-icon name="arrow" class="menu-arrow" />
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
          <span class="empty-icon">📝</span>
          <p>还没有发布动态</p>
        </div>
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import PageLayout from '@/components/layout/PageLayout.vue'
import { useAuthStore } from '@/stores/auth'
import { momentsApi } from '@/api/moments'

const authStore = useAuthStore()

// 当前用户信息
const user = ref(null)
const stats = reactive({
  moments: 0,
  friends: 0,
  likes: 0
})
const moments = ref([])
const loading = ref(true)
const loadError = ref('')

const fetchMyMoments = async () => {
  try {
    const response = await momentsApi.getMyMoments()
    const results = response.results || []
    moments.value = results
    stats.moments = response.count ?? results.length
  } catch (error) {
    console.error('获取我的动态失败:', error)
    loadError.value = '获取我的动态失败，请稍后重试'
  }
}

onMounted(async () => {
  try {
    // 优先使用已存在的用户信息，避免重复请求
    if (authStore.userInfo) {
      user.value = authStore.userInfo
    }

    // 确保用户信息最新
    const userInfo = await authStore.fetchUserInfo()
    if (userInfo) {
      user.value = userInfo
    }

    // 获取我的动态列表
    await fetchMyMoments()
  } finally {
    loading.value = false
  }
})

// 头像地址兜底：
// 1) 后端可能返回相对路径，需拼上域名
// 2) 后端在容器中返回 host.docker.internal，宿主浏览器访问不到时，替换为 localhost
const normalizeAvatar = (url) => {
  if (!url) return '/media/default_avatar.png'

  let finalUrl = url

  // 宿主访问时，如果返回的是 host.docker.internal，替换成 localhost
  if (finalUrl.includes('host.docker.internal')) {
    finalUrl = finalUrl.replace('host.docker.internal', 'localhost')
  }

  if (finalUrl.startsWith('http')) return finalUrl

  const origin = import.meta.env.VITE_API_ORIGIN || 'http://localhost:8000'
  return `${origin}${finalUrl}`
}
</script>

<style lang="scss" scoped>
.profile-page {
  min-height: 100%;
  padding-bottom: $spacing-lg;
}

.profile-header {
  position: relative;
  padding: 70px $spacing-lg $spacing-lg;
  text-align: center;
}

// 渐变背景
.profile-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 140px;
  background: $button-gradient;
  overflow: hidden;
  
  &__blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(40px);
    animation: float 20s ease-in-out infinite;
    
    &--1 {
      width: 150px;
      height: 150px;
      background: rgba($pink-primary, 0.5);
      top: -30px;
      right: -20px;
    }
    
    &--2 {
      width: 120px;
      height: 120px;
      background: rgba($baby-blue, 0.4);
      bottom: -20px;
      left: 20%;
      animation-delay: -10s;
    }
  }
  
  &::after {
    content: '';
    position: absolute;
    bottom: -40px;
    left: 0;
    right: 0;
    height: 80px;
    background: linear-gradient(to bottom, transparent, rgba(253, 247, 249, 0.8), #FDF7F9);
  }
}

.profile-info {
  position: relative;
  z-index: 1;
}

.avatar-container {
  display: inline-block;
  padding: 4px;
  background: $glass-bg-heavy;
  border-radius: 50%;
  box-shadow: $shadow-md;
}

.profile-avatar {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  object-fit: cover;
  background: linear-gradient(135deg, $pink-light, $baby-blue);
  display: block;
}

.profile-name {
  font-size: $font-size-xl;
  font-weight: $font-weight-bold;
  color: $text-primary;
  margin-top: $spacing-md;
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
  padding: 10px 18px;
  background: $glass-bg-heavy;
  backdrop-filter: $glass-blur;
  -webkit-backdrop-filter: $glass-blur;
  border: $glass-border;
  border-radius: $radius-full;
  font-size: $font-size-sm;
  font-weight: $font-weight-medium;
  color: $text-primary;
  box-shadow: $shadow-sm;
  transition: all $transition-normal;
  
  &:hover {
    background: rgba(255, 255, 255, 0.9);
    transform: translateY(-2px);
    box-shadow: $shadow-md;
  }
}

// 统计卡片 - 毛玻璃效果
.profile-stats {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: $spacing-md;
  margin: 0 $spacing-md;
  padding: $spacing-lg;
  background: $glass-bg;
  backdrop-filter: $glass-blur;
  -webkit-backdrop-filter: $glass-blur;
  border: $glass-border;
  border-radius: $radius-md;
  box-shadow: 0 4px 20px rgba(183, 168, 214, 0.2);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.stat-divider {
  width: 1px;
  height: 36px;
  background: linear-gradient(180deg, transparent, rgba($lavender, 0.3), transparent);
}

.stat-value {
  font-size: $font-size-2xl;
  font-weight: $font-weight-bold;
  color: $text-primary;
  background: $button-gradient;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: $font-size-xs;
  color: $text-muted;
  margin-top: 4px;
}

// 菜单列表
.profile-menu {
  padding: $spacing-md;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-md;
  background: $glass-bg;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: $glass-border-light;
  border-radius: $radius-lg;
  margin-bottom: $spacing-sm;
  cursor: pointer;
  transition: all $transition-normal;
  box-shadow: $shadow-sm;
  
  &:hover {
    background: $glass-bg-heavy;
    transform: translateX(4px);
  }
  
  &:active {
    transform: scale(0.98);
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
  width: 18px;
  height: 18px;
  color: $text-muted;
  transition: transform $transition-normal;
}

.menu-item:hover .menu-arrow {
  transform: translateX(4px);
}

// 我的动态
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
  gap: 6px;
}

.moment-thumb {
  aspect-ratio: 1;
  border-radius: $radius-md;
  overflow: hidden;
  cursor: pointer;
  background: $glass-bg;
  backdrop-filter: $glass-blur;
  border: $glass-border-light;
  transition: all $transition-normal;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform $transition-normal;
  }
  
  &:hover {
    transform: scale(1.02);
    box-shadow: $shadow-md;
    
    img {
      transform: scale(1.1);
    }
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
  line-height: 1.4;
}

.empty-moments {
  text-align: center;
  padding: $spacing-2xl;
  color: $text-muted;
  
  .empty-icon {
    font-size: 40px;
    display: block;
    margin-bottom: $spacing-sm;
    opacity: 0.6;
  }
  
  p {
    font-size: $font-size-sm;
  }
}
</style>
