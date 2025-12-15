<template>
  <Teleport to="body">
    <transition name="toast">
      <div v-if="visible" class="toast" :class="`toast--${type}`">
        <span class="toast__icon">
          <svg v-if="type === 'success'" viewBox="0 0 24 24" fill="currentColor">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <svg v-else-if="type === 'error'" viewBox="0 0 24 24" fill="currentColor">
            <path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <svg v-else-if="type === 'warning'" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="currentColor">
            <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </span>
        <span class="toast__message">{{ message }}</span>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'info',
    validator: (val) => ['success', 'error', 'warning', 'info'].includes(val)
  },
  duration: {
    type: Number,
    default: 3000
  },
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const visible = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  visible.value = val
  if (val && props.duration > 0) {
    setTimeout(() => {
      visible.value = false
      emit('update:modelValue', false)
    }, props.duration)
  }
})
</script>

<style lang="scss" scoped>
.toast {
  position: fixed;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: 12px 20px;
  background: $bg-card;
  border: 1px solid $border-color;
  border-radius: $radius-lg;
  box-shadow: $shadow-lg;
  z-index: $z-toast;
  
  &--success {
    border-color: rgba($success-color, 0.3);
    .toast__icon { color: $success-color; }
  }
  
  &--error {
    border-color: rgba($error-color, 0.3);
    .toast__icon { color: $error-color; }
  }
  
  &--warning {
    border-color: rgba($warning-color, 0.3);
    .toast__icon { color: $warning-color; }
  }
  
  &--info {
    border-color: rgba($info-color, 0.3);
    .toast__icon { color: $info-color; }
  }
  
  &__icon {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    
    svg {
      width: 100%;
      height: 100%;
    }
  }
  
  &__message {
    font-size: $font-size-sm;
    color: $text-primary;
  }
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-20px);
}
</style>

