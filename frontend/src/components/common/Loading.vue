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
    background: rgba($bg-dark, 0.9);
    backdrop-filter: blur(4px);
    z-index: $z-loading;
  }
  
  &__spinner {
    width: 40px;
    height: 40px;
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
  border: 3px solid $border-color;
  border-top-color: $primary-color;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>

