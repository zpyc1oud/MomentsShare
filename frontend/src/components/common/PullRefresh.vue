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
        <div 
          v-if="!isRefreshing" 
          class="pull-refresh__icon-wrapper"
          :style="{ transform: `rotate(${pullOffset >= threshold ? 180 : 0}deg)` }"
        >
          <van-icon name="arrow-down" class="pull-refresh__icon" />
        </div>
        <van-loading v-else type="spinner" size="20px" color="#FCAEC1" />
        <span class="pull-refresh__text">{{ statusText }}</span>
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
    justify-content: center;
    align-items: center;
  }
  
  &__content {
    display: flex;
    align-items: center;
    gap: $spacing-xs;
    color: $text-secondary;
    font-size: $font-size-sm;
  }
  
  &__icon-wrapper {
    transition: transform $transition-fast;
    display: flex;
    align-items: center;
  }

  &__icon {
    font-size: 20px;
    color: $text-secondary;
  }

  &__text {
    color: $text-secondary;
  }
  
  &__body {
    height: 100%;
    transition: transform $transition-normal;
    will-change: transform;
  }
}
</style>

