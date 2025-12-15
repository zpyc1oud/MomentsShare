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
          <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M15.67 4H14V2h-4v2H8.33C7.6 4 7 4.6 7 5.33v15.33C7 21.4 7.6 22 8.33 22h7.33c.74 0 1.34-.6 1.34-1.33V5.33C17 4.6 16.4 4 15.67 4z"/>
          </svg>
        </div>
      </div>
      
      <!-- 灵动岛（刘海） -->
      <div class="dynamic-island"></div>
      
      <!-- 内容区域 -->
      <div class="phone-content">
        <slot></slot>
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
  padding: 12px;
  
  // 外发光效果
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: calc(100% + 40px);
    height: calc(100% + 40px);
    background: radial-gradient(ellipse at center, rgba($primary-color, 0.15) 0%, transparent 70%);
    pointer-events: none;
    z-index: -1;
  }
}

.phone-frame {
  position: relative;
  width: $phone-width;
  height: $phone-height;
  background: $bg-dark;
  border-radius: $phone-radius;
  overflow: hidden;
  box-shadow: 
    0 0 0 2px #2a2a3e,
    0 0 0 4px #1a1a2e,
    0 0 0 6px rgba(0, 0, 0, 0.3),
    $shadow-lg,
    inset 0 0 60px rgba(0, 0, 0, 0.3);
  
  // 边框高光
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: $phone-radius;
    border: 1px solid rgba(255, 255, 255, 0.1);
    pointer-events: none;
    z-index: 1000;
  }
  
  // 侧边按钮 - 左边静音键
  &::after {
    content: '';
    position: absolute;
    left: -3px;
    top: 140px;
    width: 3px;
    height: 30px;
    background: #2a2a3e;
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
  
  .time {
    font-size: $font-size-sm;
    font-weight: $font-weight-semibold;
    letter-spacing: 0.5px;
  }
  
  .status-icons {
    display: flex;
    align-items: center;
    gap: 6px;
    
    .icon {
      width: 16px;
      height: 16px;
      opacity: 0.9;
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
  background: #000;
  border-radius: 20px;
  z-index: 200;
  
  // 摄像头指示灯
  &::after {
    content: '';
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    width: 10px;
    height: 10px;
    background: radial-gradient(circle, #1a3a5c 0%, #0a1a2c 100%);
    border-radius: 50%;
    box-shadow: inset 0 0 2px rgba(255, 255, 255, 0.2);
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
  background: $bg-dark;
}

// 底部指示条
.home-indicator {
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  width: 134px;
  height: 5px;
  background: rgba(255, 255, 255, 0.3);
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

