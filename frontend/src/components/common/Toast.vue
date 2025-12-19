<template>
  <Teleport to="body">
    <transition name="toast">
      <div v-if="visible" class="toast" :class="`toast--${type}`">
        <span class="toast__icon">
          <van-icon v-if="type === 'success'" name="success" />
          <van-icon v-else-if="type === 'error'" name="cross" />
          <van-icon v-else-if="type === 'warning'" name="warning-o" />
          <van-icon v-else name="info-o" />
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
  padding: 14px 24px;
  background: $glass-bg-heavy;
  backdrop-filter: $glass-blur;
  -webkit-backdrop-filter: $glass-blur;
  border: $glass-border;
  border-radius: $radius-full;
  box-shadow: $shadow-md;
  z-index: $z-toast;
  
  &--success {
    border-color: rgba($success-color, 0.4);
    .toast__icon { 
      color: $success-color; 
      background: rgba($success-color, 0.15);
    }
  }
  
  &--error {
    border-color: rgba($error-color, 0.4);
    .toast__icon { 
      color: $error-color; 
      background: rgba($error-color, 0.15);
    }
  }
  
  &--warning {
    border-color: rgba($warning-color, 0.4);
    .toast__icon { 
      color: $warning-color;
      background: rgba($warning-color, 0.15);
    }
  }
  
  &--info {
    border-color: rgba($baby-blue, 0.4);
    .toast__icon { 
      color: darken($baby-blue, 15%);
      background: rgba($baby-blue, 0.2);
    }
  }
  
  &__icon {
    width: 28px;
    height: 28px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-size: 18px;
  }
  
  &__message {
    font-size: $font-size-sm;
    font-weight: $font-weight-medium;
    color: $text-primary;
  }
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-30px) scale(0.9);
}
</style>
