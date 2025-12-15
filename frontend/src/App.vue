<template>
  <div class="app-container">
    <!-- 网格渐变背景 (Mesh Gradient Background) -->
    <div class="mesh-gradient-bg">
      <!-- 弥散光斑 -->
      <div class="light-blob light-blob--1"></div>
      <div class="light-blob light-blob--2"></div>
      <div class="light-blob light-blob--3"></div>
      <div class="light-blob light-blob--4"></div>
    </div>
    
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
  overflow: hidden;
  position: relative;
  background: linear-gradient(180deg, #FDF7F9 0%, #F5F0F7 50%, #F0F7FB 100%);
}

// 网格渐变背景
.mesh-gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

// 弥散光斑动画
.light-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.7;
  animation: float 20s ease-in-out infinite;
  
  &--1 {
    width: 400px;
    height: 400px;
    background: rgba(252, 174, 193, 0.5);
    top: -10%;
    left: 10%;
    animation-delay: 0s;
  }
  
  &--2 {
    width: 350px;
    height: 350px;
    background: rgba(173, 217, 243, 0.5);
    top: 10%;
    right: 5%;
    animation-delay: -5s;
  }
  
  &--3 {
    width: 300px;
    height: 300px;
    background: rgba(183, 168, 214, 0.5);
    bottom: 20%;
    left: 20%;
    animation-delay: -10s;
  }
  
  &--4 {
    width: 250px;
    height: 250px;
    background: rgba(252, 209, 219, 0.5);
    bottom: 5%;
    right: 15%;
    animation-delay: -15s;
  }
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(30px, -30px) scale(1.05);
  }
  50% {
    transform: translate(-20px, 20px) scale(0.95);
  }
  75% {
    transform: translate(-30px, -20px) scale(1.02);
  }
}

// 页面切换动画
.page-slide-enter-active,
.page-slide-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
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
