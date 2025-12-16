<template>
  <div class="loading" :class="{ 'loading--fullscreen': fullscreen }">
    <div class="loading__spinner">
      <div class="spinner"></div>
    </div>
    <p v-if="text" class="loading__text">{{ text }}</p>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: ''
  },
  fullscreen: {
    type: Boolean,
    default: false
  }
})
</script>

<style lang="scss" scoped>
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-lg;
  
  &--fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    z-index: $z-loading;
  }
  
  &__spinner {
    width: 44px;
    height: 44px;
  }
  
  &__text {
    margin-top: $spacing-md;
    font-size: $font-size-sm;
    color: $text-secondary;
  }
}

.spinner {
  width: 100%;
  height: 100%;
  border: 3px solid rgba($lavender, 0.2);
  border-top-color: $pink-primary;
  border-right-color: $lavender;
  border-radius: 50%;
  animation: spin 1s cubic-bezier(0.6, 0.2, 0.4, 0.8) infinite;
  box-shadow: 0 0 20px rgba($pink-primary, 0.2);
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
