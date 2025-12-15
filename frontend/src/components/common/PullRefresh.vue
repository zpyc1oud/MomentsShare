<template>
  <div 
    class="pull-refresh"
    @touchstart="onTouchStart"
    @touchmove="onTouchMove"
    @touchend="onTouchEnd"
  >
    <div 
      class="pull-refresh__indicator" 
      :style="{ transform: `translateY(${indicatorOffset}px)` }"
    >
      <div class="pull-refresh__content" :class="{ 'is-refreshing': isRefreshing }">
        <svg v-if="!isRefreshing" class="pull-refresh__arrow" viewBox="0 0 24 24">
          <path d="M12 5v14M5 12l7-7 7 7" stroke="currentColor" stroke-width="2" fill="none"/>
        </svg>
        <div v-else class="pull-refresh__spinner"></div>
        <span>{{ statusText }}</span>
      </div>
    </div>
    
    <div class="pull-refresh__body" :style="{ transform: `translateY(${pullOffset}px)` }">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  threshold: {
    type: Number,
    default: 60
  }
})

const emit = defineEmits(['refresh'])

const startY = ref(0)
const pullOffset = ref(0)
const isRefreshing = ref(false)
const isPulling = ref(false)

const indicatorOffset = computed(() => {
  return Math.min(pullOffset.value - 50, 10)
})

const statusText = computed(() => {
  if (isRefreshing.value) return '刷新中...'
  if (pullOffset.value >= props.threshold) return '释放刷新'
  return '下拉刷新'
})

const onTouchStart = (e) => {
  if (isRefreshing.value) return
  startY.value = e.touches[0].clientY
  isPulling.value = true
}

const onTouchMove = (e) => {
  if (!isPulling.value || isRefreshing.value) return
  
  const deltaY = e.touches[0].clientY - startY.value
  if (deltaY > 0) {
    // 阻尼效果
    pullOffset.value = deltaY * 0.5
    e.preventDefault()
  }
}

const onTouchEnd = async () => {
  if (!isPulling.value || isRefreshing.value) return
  isPulling.value = false
  
  if (pullOffset.value >= props.threshold) {
    isRefreshing.value = true
    pullOffset.value = props.threshold
    
    // 触发刷新
    emit('refresh', () => {
      isRefreshing.value = false
      pullOffset.value = 0
    })
  } else {
    pullOffset.value = 0
  }
}
</script>

<style lang="scss" scoped>
.pull-refresh {
  position: relative;
  overflow: hidden;
  height: 100%;
  
  &__indicator {
    position: absolute;
    top: -50px;
    left: 0;
    right: 0;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s ease;
  }
  
  &__content {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    font-size: $font-size-sm;
    color: $text-secondary;
    
    &.is-refreshing .pull-refresh__arrow {
      display: none;
    }
  }
  
  &__arrow {
    width: 18px;
    height: 18px;
    transition: transform 0.2s;
  }
  
  &__spinner {
    width: 18px;
    height: 18px;
    border: 2px solid $border-color;
    border-top-color: $primary-color;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  
  &__body {
    height: 100%;
    transition: transform 0.2s ease;
    overflow-y: auto;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>

