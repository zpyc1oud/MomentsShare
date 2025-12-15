<template>
  <PageLayout title="设置" :show-back="true" :show-tabbar="false">
    <div class="settings-page">
      <div class="settings-section">
        <div class="settings-item">
          <span class="settings-label">关于 MomentsShare</span>
          <span class="settings-value">v1.0.0</span>
        </div>
      </div>
      
      <div class="settings-section">
        <button class="logout-btn" @click="handleLogout">
          退出登录
        </button>
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
import { useRouter } from 'vue-router'
import PageLayout from '@/components/layout/PageLayout.vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = async () => {
  if (confirm('确定要退出登录吗？')) {
    await authStore.logout()
    router.push('/login')
  }
}
</script>

<style lang="scss" scoped>
.settings-page {
  padding: $spacing-md;
}

.settings-section {
  margin-bottom: $spacing-lg;
}

.settings-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-md;
  background: $bg-card;
  border-radius: $radius-lg;
}

.settings-label {
  font-size: $font-size-base;
  color: $text-primary;
}

.settings-value {
  font-size: $font-size-sm;
  color: $text-muted;
}

.logout-btn {
  width: 100%;
  padding: $spacing-md;
  background: rgba($error-color, 0.1);
  border: 1px solid rgba($error-color, 0.3);
  border-radius: $radius-lg;
  color: $error-color;
  font-size: $font-size-base;
  font-weight: $font-weight-medium;
  transition: all $transition-fast;
  
  &:hover {
    background: rgba($error-color, 0.2);
  }
}
</style>

