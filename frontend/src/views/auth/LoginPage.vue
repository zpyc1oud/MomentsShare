<template>
  <div class="login-page">
    <!-- 弥散光斑背景 -->
    <div class="login-bg">
      <div class="login-bg__blob login-bg__blob--1"></div>
      <div class="login-bg__blob login-bg__blob--2"></div>
      <div class="login-bg__blob login-bg__blob--3"></div>
    </div>
    
    <!-- Logo 区域 -->
    <div class="login-header">
      <div class="login-logo">
        <van-icon name="photo-o" size="36" color="#fff" />
      </div>
      <h1 class="login-title">MomentsShare</h1>
      <p class="login-subtitle">记录美好，分享生活</p>
    </div>
    
    <!-- 登录表单 - 完全使用 Vant -->
    <van-form class="login-form" @submit="handleLogin">
      <van-cell-group inset class="form-card">
        <van-field
          v-model="form.phone"
          name="phone"
          type="tel"
          placeholder="请输入手机号"
          maxlength="11"
          left-icon="phone-o"
          :rules="[
            { required: true, message: '请填写手机号' },
            { pattern: /^1\d{10}$/, message: '请输入正确的手机号' }
          ]"
          class="form-field"
        />
        
        <van-field
          v-model="form.password"
          :type="showPassword ? 'text' : 'password'"
          name="password"
          placeholder="请输入密码"
          left-icon="lock"
          :right-icon="showPassword ? 'eye-o' : 'closed-eye'"
          :rules="[{ required: true, message: '请填写密码' }]"
          class="form-field"
          @click-right-icon="showPassword = !showPassword"
        />
      </van-cell-group>
      
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      
      <div class="form-actions">
        <van-button 
          round 
          block 
          type="primary" 
          native-type="submit"
          :loading="loading"
          loading-text="登录中..."
          class="submit-btn"
        >
          登 录
        </van-button>
      </div>
    </van-form>
    
    <!-- 社交登录 -->
    <div class="social-login">
      <van-divider class="social-divider">or sign in with</van-divider>
      <div class="social-icons">
        <van-button round icon="wechat" class="social-icon-btn social-icon-btn--wechat" />
        <van-button round icon="alipay" class="social-icon-btn social-icon-btn--alipay" />
        <van-button round icon="qq" class="social-icon-btn social-icon-btn--qq" />
        <van-button round icon="weibo" class="social-icon-btn social-icon-btn--weibo" />
      </div>
    </div>
    
    <!-- 底部链接 -->
    <div class="login-footer">
      <span class="login-footer__text">还没有账号？</span>
      <router-link to="/register" class="login-footer__link">立即注册</router-link>
    </div>
    
    <!-- 用户协议 -->
    <p class="agreement-text">
      By signing up, you agree to the
      <a href="#" class="agreement-link">User Agreement</a> & 
      <a href="#" class="agreement-link">Privacy Policy</a>
    </p>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { showToast } from 'vant'

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
  loading.value = true
  errorMessage.value = ''
  
  const result = await authStore.login(form.phone, form.password)
  
  loading.value = false
  
  if (result.success) {
    showToast({
      message: '登录成功',
      type: 'success'
    })
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
  padding: $spacing-lg;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

// 弥散光斑背景
.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  
  &__blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
    
    &--1 {
      width: 220px;
      height: 220px;
      background: rgba($pink-primary, 0.4);
      top: -60px;
      right: -40px;
      animation: pulse 8s ease-in-out infinite;
    }
    
    &--2 {
      width: 180px;
      height: 180px;
      background: rgba($lavender, 0.35);
      top: 35%;
      left: -60px;
      animation: pulse 10s ease-in-out infinite;
      animation-delay: -3s;
    }
    
    &--3 {
      width: 200px;
      height: 200px;
      background: rgba($baby-blue, 0.35);
      bottom: 10%;
      right: -30px;
      animation: pulse 9s ease-in-out infinite;
      animation-delay: -5s;
    }
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.7;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.5;
  }
}

// Logo区域
.login-header {
  text-align: center;
  margin-top: 50px;
  margin-bottom: 40px;
  position: relative;
  z-index: 1;
}

.login-logo {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: $button-gradient;
  border-radius: $radius-xl;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: $shadow-glow, $shadow-inset;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 50%;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.3) 0%, transparent 100%);
    border-radius: $radius-xl $radius-xl 0 0;
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

// Vant 表单样式覆盖
.login-form {
  position: relative;
  z-index: 1;
  
  .form-card {
    background: $glass-bg-heavy;
    backdrop-filter: $glass-blur;
    -webkit-backdrop-filter: $glass-blur;
    border: $glass-border;
    border-radius: $radius-xl !important;
    overflow: hidden;
    margin: 0 !important;
  }
  
  .form-field {
    background: transparent;
    
    :deep(.van-field__body) {
      padding: 12px 0;
      align-items: center;
    }
    
    :deep(.van-field__control) {
      color: $text-primary;
      font-size: $font-size-base;
      -webkit-text-fill-color: $text-primary;
      
      &::placeholder {
        color: $text-placeholder;
        -webkit-text-fill-color: $text-placeholder;
      }
      
      // 修复浏览器自动填充导致的背景色变化
      &:-webkit-autofill,
      &:-webkit-autofill:hover,
      &:-webkit-autofill:focus,
      &:-webkit-autofill:active {
        -webkit-box-shadow: 0 0 0 1000px white inset !important;
        -webkit-text-fill-color: $text-primary !important;
        transition: background-color 5000s ease-in-out 0s;
        background-color: white !important;
        caret-color: $text-primary;
      }
    }
    
    :deep(.van-field__left-icon) {
      margin-right: 10px;
      color: $text-muted;
      font-size: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
      line-height: 1;
      
      .van-icon {
        display: flex;
        align-items: center;
        justify-content: center;
      }
    }
    
    :deep(.van-field__right-icon) {
      color: $text-muted;
      font-size: 18px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      line-height: 1;
      
      .van-icon {
        display: flex;
        align-items: center;
        justify-content: center;
      }
      
      &:hover {
        color: $text-primary;
      }
    }
  }
  
  :deep(.van-cell::after) {
    border-color: rgba($lavender, 0.2);
  }
  
  :deep(.van-field--error .van-field__control) {
    color: $error-color;
    -webkit-text-fill-color: $error-color;
  }
}

.form-actions {
  margin-top: $spacing-lg;
  padding: 0 $spacing-xs;
}

.error-message {
  color: $error-color;
  font-size: $font-size-sm;
  text-align: center;
  padding: $spacing-sm 0;
}

// 提交按钮 - 果冻质感
.submit-btn {
  height: 50px;
  font-size: $font-size-base;
  font-weight: $font-weight-semibold;
  background: $button-gradient !important;
  border: none !important;
  box-shadow: $shadow-button, $shadow-inset;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 50%;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.25) 0%, transparent 100%);
    border-radius: 25px 25px 0 0;
    pointer-events: none;
  }
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: $shadow-glow, $shadow-inset;
  }
  
  &:active:not(:disabled) {
    transform: translateY(0) scale(0.98);
  }
}

// 社交登录
.social-login {
  margin-top: $spacing-xl;
  position: relative;
  z-index: 1;
}

.social-divider {
  :deep(.van-divider__content) {
    color: $text-muted;
    font-size: $font-size-sm;
  }
  
  :deep(.van-divider::before),
  :deep(.van-divider::after) {
    border-color: rgba($lavender, 0.3);
  }
}

.social-icons {
  display: flex;
  justify-content: center;
  gap: $spacing-md;
}

.social-icon-btn {
  width: 48px !important;
  height: 48px !important;
  min-width: 48px !important;
  padding: 0 !important;
  background: $glass-bg-heavy !important;
  backdrop-filter: $glass-blur;
  -webkit-backdrop-filter: $glass-blur;
  border: $glass-border !important;
  font-size: 22px;
  box-shadow: $shadow-sm;
  
  :deep(.van-icon) {
    font-size: 22px;
  }
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: $shadow-md;
    background: rgba(255, 255, 255, 0.8) !important;
  }
  
  &:active {
    transform: translateY(0) scale(0.95);
  }
  
  &--wechat :deep(.van-icon) {
    color: #07C160;
  }
  
  &--alipay :deep(.van-icon) {
    color: #1677FF;
  }
  
  &--qq :deep(.van-icon) {
    color: #12B7F5;
  }
  
  &--weibo :deep(.van-icon) {
    color: #E6162D;
  }
}

// 底部链接
.login-footer {
  margin-top: auto;
  padding-top: $spacing-lg;
  text-align: center;
  position: relative;
  z-index: 1;
  
  &__text {
    color: $text-secondary;
    font-size: $font-size-sm;
  }
  
  &__link {
    color: $pink-primary;
    font-size: $font-size-sm;
    font-weight: $font-weight-medium;
    margin-left: 4px;
    transition: color $transition-fast;
    
    &:hover {
      color: $lavender;
    }
  }
}

// 用户协议
.agreement-text {
  margin-top: $spacing-md;
  text-align: center;
  font-size: $font-size-xs;
  color: $text-muted;
  position: relative;
  z-index: 1;
}

.agreement-link {
  color: $lavender;
  text-decoration: underline;
  
  &:hover {
    color: $pink-primary;
  }
}
</style>

