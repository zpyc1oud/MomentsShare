<template>
  <div class="register-page">
    <!-- 弥散光斑背景 -->
    <div class="register-bg">
      <div class="register-bg__blob register-bg__blob--1"></div>
      <div class="register-bg__blob register-bg__blob--2"></div>
    </div>
    
    <!-- 返回按钮 -->
    <van-nav-bar 
      left-arrow 
      @click-left="$router.back()"
      class="nav-bar"
    />
    
    <!-- 标题 -->
    <div class="register-header">
      <h1 class="register-title">Create<br/>an account</h1>
    </div>
    
    <!-- 注册表单 - 完全使用 Vant -->
    <van-form class="register-form" @submit="handleRegister">
      <van-cell-group inset class="form-card">
        <van-field
          v-model="form.nickname"
          name="nickname"
          placeholder="Full name (昵称)"
          maxlength="30"
          left-icon="user-o"
          :rules="[{ required: true, message: '请填写昵称' }]"
          class="form-field"
        />
        
        <van-field
          v-model="form.phone"
          name="phone"
          type="tel"
          placeholder="手机号"
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
          placeholder="Password (至少6位)"
          left-icon="lock"
          :right-icon="showPassword ? 'eye-o' : 'closed-eye'"
          :rules="[
            { required: true, message: '请填写密码' },
            { validator: (val) => val.length >= 6, message: '密码至少6位' }
          ]"
          class="form-field"
          @click-right-icon="showPassword = !showPassword"
        />
        
        <van-field
          v-model="form.confirmPassword"
          :type="showConfirmPassword ? 'text' : 'password'"
          name="confirmPassword"
          placeholder="Confirm Password"
          left-icon="shield-o"
          :right-icon="showConfirmPassword ? 'eye-o' : 'closed-eye'"
          :rules="[
            { required: true, message: '请确认密码' },
            { validator: (val) => val === form.password, message: '两次密码输入不一致' }
          ]"
          class="form-field"
          @click-right-icon="showConfirmPassword = !showConfirmPassword"
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
          loading-text="注册中..."
          class="submit-btn"
        >
          Sign up
        </van-button>
      </div>
    </van-form>
    
    <!-- 社交注册 -->
    <div class="social-login">
      <van-divider class="social-divider">or sign up with</van-divider>
      <div class="social-icons">
        <van-button round icon="wechat" class="social-icon-btn social-icon-btn--wechat" />
        <van-button round icon="alipay" class="social-icon-btn social-icon-btn--alipay" />
        <van-button round icon="qq" class="social-icon-btn social-icon-btn--qq" />
        <van-button round icon="weibo" class="social-icon-btn social-icon-btn--weibo" />
      </div>
    </div>
    
    <!-- 底部链接 -->
    <div class="register-footer">
      <span>Already have an account?</span>
      <router-link to="/login" class="register-footer__link">Log in</router-link>
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
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { showToast } from 'vant'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  phone: '',
  username: '',
  nickname: '',
  password: '',
  confirmPassword: ''
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

const handleRegister = async () => {
  errorMessage.value = ''
  loading.value = true
  
  // 使用昵称作为用户名（如果未单独设置）
  const username = form.username || form.phone
  
  const result = await authStore.register({
    phone: form.phone,
    username: username,
    nickname: form.nickname,
    password: form.password
  })
  
  loading.value = false
  
  if (result.success) {
    showToast({
      message: '注册成功',
      type: 'success'
    })
    router.push({ 
      path: '/login', 
      query: { message: '注册成功，请登录' } 
    })
  } else {
    errorMessage.value = result.message
  }
}
</script>

<style lang="scss" scoped>
.register-page {
  min-height: 100%;
  padding: 0 $spacing-lg $spacing-lg;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

// 弥散光斑背景
.register-bg {
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
      width: 250px;
      height: 250px;
      background: rgba($pink-primary, 0.35);
      top: -80px;
      right: -60px;
    }
    
    &--2 {
      width: 200px;
      height: 200px;
      background: rgba($baby-blue, 0.3);
      bottom: 30%;
      left: -80px;
    }
  }
}

// 导航栏
.nav-bar {
  background: transparent !important;
  position: relative;
  z-index: 1;
  
  :deep(.van-nav-bar__content) {
    height: 50px;
  }
  
  :deep(.van-nav-bar__arrow) {
    color: $text-primary;
    font-size: 22px;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: $glass-bg-heavy;
    backdrop-filter: $glass-blur;
    -webkit-backdrop-filter: $glass-blur;
    border: $glass-border;
    border-radius: 50%;
    box-shadow: $shadow-sm;
    transition: all $transition-normal;
    
    &:hover {
      transform: translateX(-2px);
      box-shadow: $shadow-md;
    }
  }
  
  :deep(.van-nav-bar__left) {
    padding-left: 0;
  }
}

// 标题区域
.register-header {
  margin-bottom: $spacing-xl;
  position: relative;
  z-index: 1;
}

.register-title {
  font-size: $font-size-3xl;
  font-weight: $font-weight-bold;
  color: $text-primary;
  line-height: 1.2;
  letter-spacing: -0.5px;
}

// Vant 表单样式覆盖
.register-form {
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
        -webkit-box-shadow: 0 0 0 30px transparent inset !important;
        -webkit-text-fill-color: $text-primary !important;
        transition: background-color 5000s ease-in-out 0s;
        caret-color: $text-primary;
      }
    }
    
    :deep(.van-field__left-icon) {
      margin-right: 10px;
      color: $text-muted;
      font-size: 18px;
      display: flex;
      align-items: center;
      height: 100%;
    }
    
    :deep(.van-field__right-icon) {
      color: $text-muted;
      font-size: 18px;
      cursor: pointer;
      display: flex;
      align-items: center;
      height: 100%;
      
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
.register-footer {
  margin-top: auto;
  padding-top: $spacing-lg;
  text-align: center;
  color: $text-secondary;
  font-size: $font-size-sm;
  position: relative;
  z-index: 1;
  
  &__link {
    color: $pink-primary;
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
