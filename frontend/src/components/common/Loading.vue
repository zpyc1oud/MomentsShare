<template>
  <div class="loading" :class="{ 'loading--fullscreen': fullscreen }">
    <van-loading type="spinner" color="#FCAEC1" size="44px" vertical>
      <template #default v-if="text">
        <span class="loading__text">{{ text }}</span>
      </template>
    </van-loading>
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
    background: rgba(255, 255, 255, 0.45);
    backdrop-filter: $glass-blur;
    -webkit-backdrop-filter: $glass-blur;
    z-index: $z-loading;
  }
  
  &__text {
    margin-top: $spacing-md;
    font-size: $font-size-sm;
    color: $text-secondary;
  }
}
</style>
