<template>
  <nav class="tabbar">
    <router-link 
      v-for="item in tabs" 
      :key="item.path" 
      :to="item.path"
      class="tabbar__item"
      :class="{ 'tabbar__item--active': isActive(item.path) }"
    >
      <div class="tabbar__icon">
        <van-icon 
          :name="isActive(item.path) ? item.activeIcon : item.icon" 
          :size="item.size || '24px'"
        />
        <span v-if="getBadge(item)" class="tabbar__badge">{{ getBadge(item) }}</span>
      </div>
      <span class="tabbar__label">{{ item.label }}</span>
    </router-link>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { friendsApi } from '@/api/friends'

const route = useRoute()

const tabs = [
  { path: '/home', label: '首页', icon: 'wap-home-o', activeIcon: 'wap-home' },
  { path: '/discover', label: '发现', icon: 'search', activeIcon: 'search' },
  { path: '/publish', label: '发布', icon: 'plus', activeIcon: 'plus', size: '26px' },
  { path: '/messages', label: '消息', icon: 'chat-o', activeIcon: 'chat' },
  { path: '/profile', label: '我的', icon: 'user-o', activeIcon: 'user' }
]

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

const isActive = (path) => {
  return route.path === path || route.path.startsWith(path + '/')
}

const getBadge = (item) => {
  if (item.path === '/messages' && pendingCount.value > 0) {
    return pendingCount.value
  }
  return null
}
</script>

<style lang="scss" scoped>
// 底部安全区域高度(home indicator)
$safe-area-bottom: 34px;

.tabbar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: calc($tabbar-height + $safe-area-bottom);
  display: flex;
  align-items: flex-start;
  justify-content: space-around;
  background: $glass-bg-heavy;
  backdrop-filter: $glass-blur;
  -webkit-backdrop-filter: $glass-blur;
  border-top: $glass-border-light;
  z-index: $z-tabbar;
  padding-top: 8px;
  padding-bottom: $safe-area-bottom;
  
  &__item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    padding: 8px 12px;
    min-width: 60px;
    color: $text-muted;
    transition: all $transition-normal;
    
    &--active {
      color: $pink-primary;
      
      .tabbar__icon {
        transform: scale(1.1);
      }
      
      .tabbar__label {
        color: $pink-primary;
      }
    }
    
    &:active {
      transform: scale(0.92);
    }
  }
  
  &__icon {
    position: relative;
    width: 24px;
    height: 24px;
    transition: transform $transition-bounce;
  }
  
  &__badge {
    position: absolute;
    top: -6px;
    right: -10px;
    min-width: 16px;
    height: 16px;
    padding: 0 4px;
    font-size: 10px;
    font-weight: $font-weight-medium;
    line-height: 16px;
    text-align: center;
    color: $text-white;
    background: linear-gradient(135deg, $pink-primary, $lavender);
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba($pink-primary, 0.4);
  }
  
  &__label {
    font-size: 10px;
    font-weight: $font-weight-medium;
    transition: color $transition-fast;
  }
}

// 发布按钮特殊样式 - 果冻质感
.tabbar__item:nth-child(3) {
  .tabbar__icon {
    width: 50px;
    height: 50px;
    background: $button-gradient;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: $shadow-glow, $shadow-inset;
    margin-top: -24px;
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 50%;
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.3) 0%, transparent 100%);
      border-radius: 50% 50% 0 0;
    }
    
    :deep(.van-icon) {
      width: 26px;
      height: 26px;
      color: white;
      position: relative;
      z-index: 1;
      font-size: 26px;
    }
  }
  
  .tabbar__label {
    display: none;
  }
  
  &:hover .tabbar__icon {
    transform: scale(1.05);
    box-shadow: 0 6px 28px rgba($pink-primary, 0.5), $shadow-inset;
  }
  
  &.tabbar__item--active .tabbar__icon {
    transform: scale(1.08) rotate(45deg);
    
    :deep(.van-icon) {
      transform: rotate(-45deg);
    }
  }
}
</style>
