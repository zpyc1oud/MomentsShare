<template>
  <Teleport to="body">
    <transition name="preview">
      <div v-if="visible" class="image-preview" @click="close">
        <div class="image-preview__header">
          <span class="image-preview__counter">{{ currentIndex + 1 }} / {{ images.length }}</span>
          <button class="image-preview__close" @click="close">
            <van-icon name="cross" />
          </button>
        </div>
        
        <div class="image-preview__body" @click.stop>
          <button 
            v-if="images.length > 1" 
            class="image-preview__nav image-preview__nav--prev"
            @click="prev"
          >
            <van-icon name="arrow-left" />
          </button>
          
          <div class="image-preview__container">
            <img 
              :src="images[currentIndex]" 
              :alt="`图片 ${currentIndex + 1}`"
              class="image-preview__image"
            />
          </div>
          
          <button 
            v-if="images.length > 1" 
            class="image-preview__nav image-preview__nav--next"
            @click="next"
          >
            <van-icon name="arrow" />
          </button>
        </div>
        
        <div v-if="images.length > 1" class="image-preview__dots">
          <span 
            v-for="(_, index) in images" 
            :key="index"
            class="image-preview__dot"
            :class="{ 'image-preview__dot--active': index === currentIndex }"
            @click.stop="currentIndex = index"
          ></span>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    default: () => []
  },
  startIndex: {
    type: Number,
    default: 0
  },
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const visible = ref(props.modelValue)
const currentIndex = ref(props.startIndex)

watch(() => props.modelValue, (val) => {
  visible.value = val
  if (val) {
    currentIndex.value = props.startIndex
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

const close = () => {
  visible.value = false
  emit('update:modelValue', false)
}

const prev = () => {
  currentIndex.value = currentIndex.value > 0 
    ? currentIndex.value - 1 
    : props.images.length - 1
}

const next = () => {
  currentIndex.value = currentIndex.value < props.images.length - 1 
    ? currentIndex.value + 1 
    : 0
}
</script>

<style lang="scss" scoped>
.image-preview {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.95);
  z-index: $z-modal;
  display: flex;
  flex-direction: column;
  
  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: $spacing-md;
  }
  
  &__counter {
    font-size: $font-size-sm;
    color: $text-secondary;
  }
  
  &__close {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    
    svg {
      width: 20px;
      height: 20px;
    }
  }
  
  &__body {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 0 $spacing-xl;
  }
  
  &__container {
    max-width: 100%;
    max-height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  &__image {
    max-width: 100%;
    max-height: 70vh;
    object-fit: contain;
    border-radius: $radius-sm;
  }
  
  &__nav {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    transition: background $transition-fast;
    color: white;
    font-size: 24px;
    
    &:hover {
      background: rgba(255, 255, 255, 0.2);
    }
    
    &--prev { left: $spacing-md; }
    &--next { right: $spacing-md; }
  }
  
  &__dots {
    display: flex;
    justify-content: center;
    gap: $spacing-sm;
    padding: $spacing-md;
  }
  
  &__dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    cursor: pointer;
    transition: all $transition-fast;
    
    &--active {
      width: 20px;
      border-radius: 3px;
      background: $pink-primary;
    }
  }
}

.preview-enter-active,
.preview-leave-active {
  transition: opacity 0.3s ease;
}

.preview-enter-from,
.preview-leave-to {
  opacity: 0;
}
</style>

