<template>
  <div class="register-page">
    <!-- 返回按钮 -->
    <button class="back-btn" @click="$router.back()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M15 18l-6-6 6-6"/>
      </svg>
    </button>
    
    <!-- 标题 -->
    <div class="register-header">
      <h1 class="register-title">创建账号</h1>
      <p class="register-subtitle">加入 MomentsShare，开始分享生活</p>
    </div>
    
    <!-- 注册表单 -->
    <form class="register-form" @submit.prevent="handleRegister">
      <div class="form-group">
        <label class="form-label">手机号</label>
        <input 
          v-model="form.phone"
          type="tel"
          class="form-input"
          placeholder="请输入11位手机号"
          maxlength="11"
        />
      </div>
      
      <div class="form-group">
        <label class="form-label">用户名</label>
        <input 
          v-model="form.username"
          type="text"
          class="form-input"
          placeholder="用于登录和识别，不可重复"
          maxlength="30"
        />
      </div>
      
      <div class="form-group">
        <label class="form-label">昵称</label>
        <input 
          v-model="form.nickname"
          type="text"
          class="form-input"
          placeholder="显示给其他用户看的名称"
          maxlength="30"
        />
      </div>
      
      <div class="form-group">
        <label class="form-label">密码</label>
        <input 
          v-model="form.password"
          type="password"
          class="form-input"
          placeholder="请设置登录密码"
        />
      </div>
      
      <div class="form-group">
        <label class="form-label">确认密码</label>
        <input 
          v-model="form.confirmPassword"
          type="password"
          class="form-input"
          placeholder="请再次输入密码"
        />
      </div>
      
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      
      <button type="submit" class="btn btn--primary btn--block" :disabled="loading">
        {{ loading ? '注册中...' : '注 册' }}
      </button>
    </form>
    
    <!-- 底部链接 -->
    <div class="register-footer">
      <span>已有账号？</span>
      <router-link to="/login" class="register-footer__link">立即登录</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  phone: '',
  username: '',
  nickname: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const errorMessage = ref('')

const validateForm = () => {
  if (!form.phone || !form.username || !form.nickname || !form.password) {
    errorMessage.value = '请填写所有必填项'
    return false
  }
  
  if (!/^1\d{10}$/.test(form.phone)) {
    errorMessage.value = '请输入正确的手机号'
    return false
  }
  
  if (form.password.length < 6) {
    errorMessage.value = '密码至少6位'
    return false
  }
  
  if (form.password !== form.confirmPassword) {
    errorMessage.value = '两次密码输入不一致'
    return false
  }
  
  return true
}

const handleRegister = async () => {
  errorMessage.value = ''
  
  if (!validateForm()) return
  
  loading.value = true
  
  const result = await authStore.register({
    phone: form.phone,
    username: form.username,
    nickname: form.nickname,
    password: form.password
  })
  
  loading.value = false
  
  if (result.success) {
    // 注册成功，跳转登录
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
  padding: $spacing-md $spacing-lg;
  display: flex;
  flex-direction: column;
}

.back-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: $spacing-md;
  
  svg {
    width: 24px;
    height: 24px;
  }
}

.register-header {
  margin-bottom: $spacing-xl;
}

.register-title {
  font-size: $font-size-2xl;
  font-weight: $font-weight-bold;
  color: $text-primary;
  margin-bottom: 8px;
}

.register-subtitle {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: $font-size-sm;
  font-weight: $font-weight-medium;
  color: $text-secondary;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  background: $bg-input;
  border: 1px solid $border-color;
  border-radius: $radius-md;
  color: $text-primary;
  font-size: $font-size-base;
  transition: all $transition-fast;
  
  &:focus {
    border-color: $primary-color;
    box-shadow: 0 0 0 3px rgba($primary-color, 0.1);
  }
  
  &::placeholder {
    color: $text-placeholder;
  }
}

.error-message {
  color: $error-color;
  font-size: $font-size-sm;
  text-align: center;
}

.register-footer {
  margin-top: auto;
  padding-top: $spacing-xl;
  text-align: center;
  color: $text-secondary;
  font-size: $font-size-sm;
  
  &__link {
    color: $primary-color;
    font-weight: $font-weight-medium;
    margin-left: 4px;
  }
}
</style>

