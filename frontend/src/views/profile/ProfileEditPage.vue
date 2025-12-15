<template>
  <PageLayout title="编辑资料" :show-back="true" :show-tabbar="false">
    <template #nav-right>
      <button class="save-btn" :disabled="saving" @click="handleSave">
        {{ saving ? '保存中...' : '保存' }}
      </button>
    </template>
    
    <div class="edit-page">
      <!-- 头像修改 -->
      <div class="edit-section">
        <label class="avatar-upload">
          <img :src="avatarPreview || user?.avatar || '/default-avatar.png'" class="edit-avatar" />
          <div class="avatar-overlay">
            <span>更换头像</span>
          </div>
          <input type="file" accept="image/*" hidden @change="handleAvatarChange" />
        </label>
      </div>
      
      <!-- 基本信息 -->
      <div class="edit-section">
        <div class="edit-item">
          <label class="edit-label">用户名</label>
          <input 
            v-model="form.username"
            type="text"
            class="edit-input"
            placeholder="请输入用户名"
            maxlength="30"
          />
        </div>
        
        <div class="edit-item">
          <label class="edit-label">昵称</label>
          <input 
            v-model="form.nickname"
            type="text"
            class="edit-input"
            placeholder="请输入昵称"
            maxlength="30"
          />
        </div>
        
        <div class="edit-item" @click="showPhoneModal = true">
          <label class="edit-label">手机号</label>
          <div class="edit-value">
            {{ maskPhone(user?.phone) }}
            <svg class="edit-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 18l6-6-6-6"/>
            </svg>
          </div>
        </div>
      </div>
      
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
    
    <!-- 修改手机号弹窗 -->
    <Modal v-model="showPhoneModal" title="修改手机号">
      <div class="phone-form">
        <div class="form-group">
          <label class="form-label">当前密码</label>
          <input 
            v-model="phoneForm.password"
            type="password"
            class="form-input"
            placeholder="请输入当前登录密码"
          />
        </div>
        <div class="form-group">
          <label class="form-label">新手机号</label>
          <input 
            v-model="phoneForm.new_phone"
            type="tel"
            class="form-input"
            placeholder="请输入新手机号"
            maxlength="11"
          />
        </div>
        <p v-if="phoneError" class="error-message">{{ phoneError }}</p>
      </div>
      
      <template #footer>
        <button class="btn btn--secondary" @click="showPhoneModal = false">取消</button>
        <button class="btn btn--primary" :disabled="changingPhone" @click="changePhone">
          {{ changingPhone ? '提交中...' : '确认修改' }}
        </button>
      </template>
    </Modal>
  </PageLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PageLayout from '@/components/layout/PageLayout.vue'
import Modal from '@/components/common/Modal.vue'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/api/auth'

const router = useRouter()
const authStore = useAuthStore()

const user = ref(null)
const avatarFile = ref(null)
const avatarPreview = ref('')
const saving = ref(false)
const errorMessage = ref('')

const form = reactive({
  username: '',
  nickname: ''
})

const showPhoneModal = ref(false)
const phoneForm = reactive({
  password: '',
  new_phone: ''
})
const phoneError = ref('')
const changingPhone = ref(false)

onMounted(async () => {
  const userInfo = await authStore.fetchUserInfo()
  if (userInfo) {
    user.value = userInfo
    form.username = userInfo.username
    form.nickname = userInfo.nickname
  }
})

const handleAvatarChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    avatarFile.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      avatarPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const handleSave = async () => {
  if (!form.username || !form.nickname) {
    errorMessage.value = '用户名和昵称不能为空'
    return
  }
  
  saving.value = true
  errorMessage.value = ''
  
  try {
    const data = {
      username: form.username,
      nickname: form.nickname
    }
    
    if (avatarFile.value) {
      data.avatar = avatarFile.value
    }
    
    await authApi.updateUserInfo(data)
    await authStore.fetchUserInfo()
    
    router.back()
  } catch (error) {
    const errors = error.response?.data?.detail || {}
    errorMessage.value = Object.values(errors).flat()[0] || '保存失败'
  } finally {
    saving.value = false
  }
}

const maskPhone = (phone) => {
  if (!phone) return ''
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

const changePhone = async () => {
  if (!phoneForm.password || !phoneForm.new_phone) {
    phoneError.value = '请填写完整信息'
    return
  }
  
  if (!/^1\d{10}$/.test(phoneForm.new_phone)) {
    phoneError.value = '请输入正确的手机号'
    return
  }
  
  changingPhone.value = true
  phoneError.value = ''
  
  try {
    await authApi.changePhone(phoneForm)
    await authStore.fetchUserInfo()
    
    showPhoneModal.value = false
    phoneForm.password = ''
    phoneForm.new_phone = ''
  } catch (error) {
    const errors = error.response?.data?.detail || {}
    phoneError.value = Object.values(errors).flat()[0] || '修改失败'
  } finally {
    changingPhone.value = false
  }
}
</script>

<style lang="scss" scoped>
.edit-page {
  padding: $spacing-md;
}

.save-btn {
  padding: 8px 16px;
  background: $primary-gradient;
  border-radius: $radius-full;
  font-size: $font-size-sm;
  font-weight: $font-weight-medium;
  
  &:disabled {
    opacity: 0.5;
  }
}

.edit-section {
  margin-bottom: $spacing-lg;
}

.avatar-upload {
  display: block;
  width: 100px;
  height: 100px;
  margin: 0 auto;
  position: relative;
  cursor: pointer;
}

.edit-avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 6px;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 0 0 50px 50px;
  text-align: center;
  font-size: $font-size-xs;
  color: $text-primary;
}

.edit-item {
  display: flex;
  align-items: center;
  padding: $spacing-md 0;
  border-bottom: 1px solid $border-light;
}

.edit-label {
  width: 80px;
  font-size: $font-size-base;
  color: $text-secondary;
  flex-shrink: 0;
}

.edit-input {
  flex: 1;
  padding: 8px 0;
  font-size: $font-size-base;
  color: $text-primary;
  text-align: right;
  
  &::placeholder {
    color: $text-placeholder;
  }
}

.edit-value {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: $spacing-xs;
  font-size: $font-size-base;
  color: $text-primary;
  cursor: pointer;
}

.edit-arrow {
  width: 18px;
  height: 18px;
  color: $text-muted;
}

.error-message {
  color: $error-color;
  font-size: $font-size-sm;
  text-align: center;
  margin-top: $spacing-md;
}

.phone-form {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
}

.form-label {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.form-input {
  padding: 12px;
  background: $bg-input;
  border: 1px solid $border-color;
  border-radius: $radius-md;
  color: $text-primary;
  font-size: $font-size-base;
  
  &:focus {
    border-color: $primary-color;
  }
}
</style>

