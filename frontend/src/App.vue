<template>
  <div class="app-container">
    <!-- 手机模拟器外壳 -->
    <PhoneSimulator>
      <router-view v-slot="{ Component }">
        <transition name="page-slide" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </PhoneSimulator>
  </div>
</template>

<script setup>
import PhoneSimulator from '@/components/layout/PhoneSimulator.vue'
</script>

<style lang="scss">
.app-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  overflow: hidden;
}

// 页面切换动画
.page-slide-enter-active,
.page-slide-leave-active {
  transition: all 0.3s ease;
}

.page-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.page-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>

