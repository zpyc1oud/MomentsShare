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
        <component :is="item.icon" :filled="isActive(item.path)" />
        <span v-if="item.badge" class="tabbar__badge">{{ item.badge }}</span>
      </div>
      <span class="tabbar__label">{{ item.label }}</span>
    </router-link>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import IconHome from '@/components/icons/IconHome.vue'
import IconSearch from '@/components/icons/IconSearch.vue'
import IconAdd from '@/components/icons/IconAdd.vue'
import IconMessage from '@/components/icons/IconMessage.vue'
import IconProfile from '@/components/icons/IconProfile.vue'

const route = useRoute()

const tabs = [
  { path: '/home', label: '首页', icon: IconHome },
  { path: '/discover', label: '发现', icon: IconSearch },
  { path: '/publish', label: '发布', icon: IconAdd },
  { path: '/messages', label: '消息', icon: IconMessage },
  { path: '/profile', label: '我的', icon: IconProfile }
]

const isActive = (path) => {
  return route.path === path || route.path.startsWith(path + '/')
}
</script>

<style lang="scss" scoped>
.tabbar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: $tabbar-height;
  display: flex;
  align-items: center;
  justify-content: space-around;
  background: rgba($bg-dark, 0.95);
  backdrop-filter: blur(20px);
  border-top: 1px solid $border-light;
  z-index: $z-tabbar;
  
  &__item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    padding: 8px 12px;
    min-width: 60px;
    color: $text-muted;
    transition: all $transition-fast;
    
    &--active {
      color: $primary-color;
      
      .tabbar__icon {
        transform: scale(1.1);
      }
    }
    
    &:active {
      transform: scale(0.95);
    }
  }
  
  &__icon {
    position: relative;
    width: 24px;
    height: 24px;
    transition: transform $transition-fast;
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
    color: $text-primary;
    background: $error-color;
    border-radius: 8px;
  }
  
  &__label {
    font-size: 10px;
    font-weight: $font-weight-medium;
  }
}

// 发布按钮特殊样式
.tabbar__item:nth-child(3) {
  .tabbar__icon {
    width: 44px;
    height: 44px;
    background: $primary-gradient;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba($primary-color, 0.4);
    margin-top: -20px;
    
    :deep(svg) {
      width: 24px;
      height: 24px;
      color: white;
    }
  }
  
  .tabbar__label {
    display: none;
  }
  
  &.tabbar__item--active .tabbar__icon {
    transform: scale(1.05) rotate(45deg);
  }
}
</style>

