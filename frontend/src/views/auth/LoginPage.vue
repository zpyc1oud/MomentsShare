<template>
  <div class="login-page">
    <!-- 背景装饰 -->
    <div class="login-bg">
      <div class="login-bg__circle login-bg__circle--1"></div>
      <div class="login-bg__circle login-bg__circle--2"></div>
    </div>
    
    <!-- Logo 区域 -->
    <div class="login-header">
      <div class="login-logo">
        <span class="logo-icon">📸</span>
      </div>
      <h1 class="login-title">MomentsShare</h1>
      <p class="login-subtitle">记录美好，分享生活</p>
    </div>
    
    <!-- 登录表单 -->
    <form class="login-form" @submit.prevent="handleLogin">
      <div class="input-wrapper">
        <span class="input-icon">📱</span>
        <input 
          v-model="form.phone"
          type="tel"
          class="input"
          placeholder="请输入手机号"
          maxlength="11"
        />
      </div>
      
      <div class="input-wrapper">
        <span class="input-icon">🔒</span>
        <input 
          v-model="form.password"
          :type="showPassword ? 'text' : 'password'"
          class="input"
          placeholder="请输入密码"
        />
        <button 
          type="button" 
          class="input-toggle"
          @click="showPassword = !showPassword"
        >
          {{ showPassword ? '🙈' : '👁️' }}
        </button>
      </div>
      
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      
      <button type="submit" class="btn btn--primary btn--block" :disabled="loading">
        {{ loading ? '登录中...' : '登 录' }}
      </button>
    </form>
    
    <!-- 底部链接 -->
    <div class="login-footer">
      <span class="login-footer__text">还没有账号？</span>
      <router-link to="/register" class="login-footer__link">立即注册</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = reactive({
  phone: '',
  password: ''
})

const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  if (!form.phone || !form.password) {
    errorMessage.value = '请填写手机号和密码'
    return
  }
  
  if (!/^1\d{10}$/.test(form.phone)) {
    errorMessage.value = '请输入正确的手机号'
    return
  }
  
  loading.value = true
  errorMessage.value = ''
  
  const result = await authStore.login(form.phone, form.password)
  
  loading.value = false
  
  if (result.success) {
    const redirect = route.query.redirect || '/home'
    router.push(redirect)
  } else {
    errorMessage.value = result.message
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100%;
  padding: $spacing-xl $spacing-lg;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  
  &__circle {
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
    
    &--1 {
      width: 200px;
      height: 200px;
      background: rgba($primary-color, 0.3);
      top: -50px;
      right: -50px;
    }
    
    &--2 {
      width: 150px;
      height: 150px;
      background: rgba($accent-color, 0.2);
      bottom: 100px;
      left: -30px;
    }
  }
}

.login-header {
  text-align: center;
  margin-top: 60px;
  margin-bottom: 50px;
  position: relative;
  z-index: 1;
}

.login-logo {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: $primary-gradient;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: $shadow-glow;
  
  .logo-icon {
    font-size: 36px;
  }
}

.login-title {
  font-size: $font-size-2xl;
  font-weight: $font-weight-bold;
  color: $text-primary;
  margin-bottom: 8px;
  letter-spacing: 1px;
}

.login-subtitle {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
  position: relative;
  z-index: 1;
  
  .input-wrapper {
    position: relative;
    
    .input {
      width: 100%;
      padding: 16px 16px 16px 48px;
      background: $bg-input;
      border: 1px solid $border-color;
      border-radius: $radius-lg;
      color: $text-primary;
      font-size: $font-size-base;
      transition: all $transition-fast;
      
      &:focus {
        border-color: $primary-color;
        box-shadow: 0 0 0 3px rgba($primary-color, 0.1);
      }
    }
    
    .input-icon {
      position: absolute;
      left: 16px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 18px;
    }
    
    .input-toggle {
      position: absolute;
      right: 16px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 18px;
      opacity: 0.7;
    }
  }
}

.error-message {
  color: $error-color;
  font-size: $font-size-sm;
  text-align: center;
}

.login-footer {
  margin-top: auto;
  padding-top: $spacing-xl;
  text-align: center;
  position: relative;
  z-index: 1;
  
  &__text {
    color: $text-secondary;
    font-size: $font-size-sm;
  }
  
  &__link {
    color: $primary-color;
    font-size: $font-size-sm;
    font-weight: $font-weight-medium;
    margin-left: 4px;
  }
}
</style>

