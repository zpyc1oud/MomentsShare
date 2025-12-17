<template>
  <div class="phone-simulator">
    <!-- 手机外壳 -->
    <div class="phone-frame">
      <!-- 状态栏 -->
      <div class="status-bar">
        <span class="time">{{ currentTime }}</span>
        <div class="status-icons">
          <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12.01 21.49L23.64 7c-.45-.34-4.93-4-11.64-4C5.28 3 .81 6.66.36 7l11.63 14.49.01.01.01-.01z"/>
          </svg>
          <span class="battery-text">70</span>
          <svg class="icon icon--battery" viewBox="0 0 24 24" fill="currentColor">
            <path d="M15.67 4H14V2h-4v2H8.33C7.6 4 7 4.6 7 5.33v15.33C7 21.4 7.6 22 8.33 22h7.33c.74 0 1.34-.6 1.34-1.33V5.33C17 4.6 16.4 4 15.67 4z"/>
          </svg>
        </div>
      </div>
      
      <!-- 灵动岛（刘海） -->
      <div class="dynamic-island"></div>
      
      <!-- 内容区域 -->
      <div class="phone-content">
        <!-- 内容区网格渐变背景 -->
        <div class="content-bg">
          <div class="content-blob content-blob--1"></div>
          <div class="content-blob content-blob--2"></div>
          <div class="content-blob content-blob--3"></div>
        </div>
        <div class="content-wrapper">
          <slot></slot>
        </div>
      </div>
      
      <!-- 底部指示条 -->
      <div class="home-indicator"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const currentTime = ref('')

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: false 
  })
}

let timer = null

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style lang="scss" scoped>
.phone-simulator {
  position: relative;
  padding: 16px;
  
  // 柔和外发光效果
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: calc(100% + 60px);
    height: calc(100% + 60px);
    background: radial-gradient(ellipse at center, 
      rgba($pink-primary, 0.15) 0%, 
      rgba($lavender, 0.1) 30%,
      transparent 70%
    );
    pointer-events: none;
    z-index: -1;
  }
}

.phone-frame {
  position: relative;
  width: $phone-width;
  height: $phone-height;
  background: linear-gradient(180deg, #FDF7F9 0%, #F8F4F9 50%, #F5F8FC 100%);
  border-radius: $phone-radius;
  overflow: hidden;
  box-shadow: 
    0 0 0 1px rgba(255, 255, 255, 0.8),
    0 0 0 2px rgba($lavender, 0.2),
    0 25px 50px rgba($lavender, 0.25),
    0 10px 30px rgba($pink-primary, 0.1),
    inset 0 0 80px rgba(255, 255, 255, 0.5);
  
  // 边框高光
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: $phone-radius;
    border: 1px solid rgba(255, 255, 255, 0.6);
    pointer-events: none;
    z-index: 1000;
  }
  
  // 侧边按钮
  &::after {
    content: '';
    position: absolute;
    left: -3px;
    top: 140px;
    width: 3px;
    height: 30px;
    background: linear-gradient(180deg, rgba($lavender, 0.4), rgba($lavender, 0.2));
    border-radius: 2px 0 0 2px;
  }
}

// 状态栏
.status-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: $status-bar-height;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 28px 0;
  z-index: 100;
  color: $text-primary;
  
  .time {
    font-size: $font-size-sm;
    font-weight: $font-weight-semibold;
    letter-spacing: 0.5px;
  }
  
  .status-icons {
    display: flex;
    align-items: center;
    gap: 4px;
    
    .icon {
      width: 16px;
      height: 16px;
      opacity: 0.85;
      
      &--battery {
        width: 20px;
      }
    }
    
    .battery-text {
      font-size: 11px;
      font-weight: $font-weight-medium;
    }
  }
}

// 灵动岛
.dynamic-island {
  position: absolute;
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
  width: $phone-notch-width;
  height: $phone-notch-height;
  background: #1a1a1e;
  border-radius: 20px;
  z-index: 200;
  
  // 摄像头
  &::after {
    content: '';
    position: absolute;
    right: 22px;
    top: 50%;
    transform: translateY(-50%);
    width: 10px;
    height: 10px;
    background: radial-gradient(circle, #2a3a5c 0%, #1a2a3c 100%);
    border-radius: 50%;
    box-shadow: inset 0 0 2px rgba(255, 255, 255, 0.15);
  }
}

// 内容区域
.phone-content {
  position: absolute;
  top: $status-bar-height;
  left: 0;
  right: 0;
  bottom: 34px;
  overflow: hidden;
  background: transparent;
}

// 内容区网格渐变背景
.content-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

.content-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(50px);
  opacity: 0.6;
  
  &--1 {
    width: 200px;
    height: 200px;
    background: rgba($pink-primary, 0.35);
    top: -50px;
    right: -30px;
  }
  
  &--2 {
    width: 180px;
    height: 180px;
    background: rgba($baby-blue, 0.3);
    top: 40%;
    left: -50px;
  }
  
  &--3 {
    width: 160px;
    height: 160px;
    background: rgba($lavender, 0.35);
    bottom: -30px;
    right: 20%;
  }
}

.content-wrapper {
  position: relative;
  height: 100%;
  z-index: 1;
}

// 底部指示条
.home-indicator {
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  width: 134px;
  height: 5px;
  background: rgba($text-primary, 0.25);
  border-radius: 3px;
}

// 响应式处理
@media (max-height: 900px) {
  .phone-frame {
    transform: scale(0.85);
    transform-origin: center center;
  }
}

@media (max-height: 750px) {
  .phone-frame {
    transform: scale(0.75);
  }
}
</style>
