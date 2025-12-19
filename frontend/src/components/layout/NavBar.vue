<template>
  <header class="navbar" :class="{ 'navbar--transparent': transparent }">
    <div class="navbar__left">
      <button v-if="showBack" class="navbar__back" @click="$emit('back')">
        <van-icon name="arrow-left" />
      </button>
      <slot name="left"></slot>
    </div>
    
    <h1 class="navbar__title">{{ title }}</h1>
    
    <div class="navbar__right">
      <slot name="right"></slot>
    </div>
  </header>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  showBack: {
    type: Boolean,
    default: false
  },
  transparent: {
    type: Boolean,
    default: false
  }
})

defineEmits(['back'])
</script>

<style lang="scss" scoped>
.navbar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: $navbar-height;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 $spacing-md;
  background: $glass-bg-heavy;
  backdrop-filter: $glass-blur;
  -webkit-backdrop-filter: $glass-blur;
  border-bottom: $glass-border-light;
  z-index: $z-navbar;
  transition: all $transition-normal;
  
  &--transparent {
    background: transparent;
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
    border-bottom-color: transparent;
  }
  
  &__left,
  &__right {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    min-width: 60px;
  }
  
  &__right {
    justify-content: flex-end;
  }
  
  &__back {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    background: $glass-bg;
    backdrop-filter: $glass-blur;
    -webkit-backdrop-filter: $glass-blur;
    border: $glass-border-light;
    border-radius: 50%;
    transition: all $transition-normal;
    box-shadow: 0 4px 12px rgba(183, 168, 214, 0.2);
    
    svg {
      width: 20px;
      height: 20px;
      color: $text-primary;
    }
    
    &:hover {
      background: rgba(255, 255, 255, 0.7);
      transform: translateX(-2px);
      box-shadow: 0 6px 16px rgba(183, 168, 214, 0.3);
    }
    
    &:active {
      transform: scale(0.95);
    }
  }
  
  &__title {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    font-size: $font-size-lg;
    font-weight: $font-weight-semibold;
    color: $text-primary;
    max-width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
</style>
