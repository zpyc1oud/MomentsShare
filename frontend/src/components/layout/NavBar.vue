<template>
  <header class="navbar" :class="{ 'navbar--transparent': transparent }">
    <div class="navbar__left">
      <button v-if="showBack" class="navbar__back" @click="$emit('back')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M15 18l-6-6 6-6"/>
        </svg>
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
  background: $bg-dark;
  border-bottom: 1px solid $border-light;
  z-index: $z-navbar;
  transition: background $transition-normal;
  
  &--transparent {
    background: transparent;
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
    width: 36px;
    height: 36px;
    border-radius: 50%;
    transition: background $transition-fast;
    
    svg {
      width: 22px;
      height: 22px;
    }
    
    &:hover {
      background: rgba(255, 255, 255, 0.1);
    }
    
    &:active {
      background: rgba(255, 255, 255, 0.15);
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

