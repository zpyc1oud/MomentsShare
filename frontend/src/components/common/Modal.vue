<template>
  <Teleport to="body">
    <transition name="modal">
      <div v-if="modelValue" class="modal-backdrop" @click="handleBackdropClick">
        <div 
          class="modal" 
          :class="[`modal--${size}`]"
          @click.stop
        >
          <div v-if="showHeader" class="modal__header">
            <h3 class="modal__title">{{ title }}</h3>
            <button v-if="showClose" class="modal__close" @click="close">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
            </button>
          </div>
          
          <div class="modal__body">
            <slot></slot>
          </div>
          
          <div v-if="$slots.footer" class="modal__footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'default',
    validator: (val) => ['small', 'default', 'large'].includes(val)
  },
  showHeader: {
    type: Boolean,
    default: true
  },
  showClose: {
    type: Boolean,
    default: true
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

watch(() => props.modelValue, (val) => {
  document.body.style.overflow = val ? 'hidden' : ''
})

const close = () => {
  emit('update:modelValue', false)
  emit('close')
}

const handleBackdropClick = () => {
  if (props.closeOnBackdrop) {
    close()
  }
}
</script>

<style lang="scss" scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-lg;
  z-index: $z-modal;
}

.modal {
  width: 100%;
  background: $bg-card;
  border-radius: $radius-xl;
  border: 1px solid $border-color;
  box-shadow: $shadow-lg;
  overflow: hidden;
  
  &--small {
    max-width: 300px;
  }
  
  &--default {
    max-width: 360px;
  }
  
  &--large {
    max-width: 420px;
  }
  
  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: $spacing-md $spacing-lg;
    border-bottom: 1px solid $border-light;
  }
  
  &__title {
    font-size: $font-size-lg;
    font-weight: $font-weight-semibold;
    color: $text-primary;
  }
  
  &__close {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    color: $text-muted;
    transition: all $transition-fast;
    
    svg {
      width: 18px;
      height: 18px;
    }
    
    &:hover {
      background: rgba(255, 255, 255, 0.1);
      color: $text-primary;
    }
  }
  
  &__body {
    padding: $spacing-lg;
  }
  
  &__footer {
    display: flex;
    justify-content: flex-end;
    gap: $spacing-sm;
    padding: $spacing-md $spacing-lg;
    border-top: 1px solid $border-light;
  }
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
  
  .modal {
    transition: all 0.3s ease;
  }
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  
  .modal {
    transform: scale(0.95) translateY(20px);
  }
}
</style>

