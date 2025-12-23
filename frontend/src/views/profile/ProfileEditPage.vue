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
        <div class="avatar-wrapper">
          <label class="avatar-upload">
            <img :src="avatarPreview || normalizeAvatar(user?.avatar)" class="edit-avatar" />
            <div class="avatar-overlay">
              <span>{{ avatarFile ? '重新选择' : '更换头像' }}</span>
            </div>
            <input type="file" accept="image/jpeg,image/jpg,image/png,image/gif,image/webp" hidden @change="handleAvatarChange" />
          </label>
          <button 
            v-if="avatarFile" 
            class="avatar-clear-btn" 
            @click="clearAvatar"
            type="button"
          >
            取消
          </button>
        </div>
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
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

// 记录初始值，用于判断是否有改动
const initialForm = reactive({
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

const currentPhone = computed(() => user.value?.phone || '')

onMounted(async () => {
  const userInfo = await authStore.fetchUserInfo()
  if (userInfo) {
    user.value = userInfo
    form.username = userInfo.username
    form.nickname = userInfo.nickname
    initialForm.username = userInfo.username
    initialForm.nickname = userInfo.nickname
  }
})

// 头像地址兜底：
// 1) 后端可能返回相对路径，需拼上域名
// 2) 后端在容器中返回 host.docker.internal，宿主浏览器访问不到时，替换为 localhost
const normalizeAvatar = (url) => {
  if (!url) return '/media/default_avatar.png'

  let finalUrl = url

  // 宿主访问时，如果返回的是 host.docker.internal，替换成 localhost
  if (finalUrl.includes('host.docker.internal')) {
    finalUrl = finalUrl.replace('host.docker.internal', 'localhost')
  }

  if (finalUrl.startsWith('http')) return finalUrl

  const origin = import.meta.env.VITE_API_ORIGIN || 'http://localhost:8000'
  return `${origin}${finalUrl}`
}

const handleAvatarChange = (e) => {
  const file = e.target.files[0]
  if (!file) return

  // 文件类型校验
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    showToast({
      message: '请选择图片文件（JPG、PNG、GIF、WebP）',
      type: 'fail'
    })
    e.target.value = '' // 清空文件选择
    return
  }

  // 文件大小校验（限制 5MB）
  const maxSize = 5 * 1024 * 1024 // 5MB
  if (file.size > maxSize) {
    showToast({
      message: '图片大小不能超过 5MB',
      type: 'fail'
    })
    e.target.value = ''
    return
  }

  // 文件大小过小提示（小于 1KB 可能是无效文件）
  if (file.size < 1024) {
    showToast({
      message: '图片文件可能无效，请重新选择',
      type: 'fail'
    })
    e.target.value = ''
    return
  }

  // 保存文件并生成预览
  avatarFile.value = file
  const reader = new FileReader()
  reader.onload = (e) => {
    avatarPreview.value = e.target.result
  }
  reader.onerror = () => {
    showToast({
      message: '图片读取失败，请重新选择',
      type: 'fail'
    })
    avatarFile.value = null
    avatarPreview.value = ''
  }
  reader.readAsDataURL(file)
}

const clearAvatar = () => {
  avatarFile.value = null
  avatarPreview.value = ''
  // 清空文件输入框
  const fileInput = document.querySelector('input[type="file"]')
  if (fileInput) {
    fileInput.value = ''
  }
}

const handleSave = async () => {
  const username = (form.username || '').trim()
  const nickname = (form.nickname || '').trim()

  // 基础校验
  if (!username || !nickname) {
    errorMessage.value = '用户名和昵称不能为空'
    return
  }

  if (username.length < 3 || username.length > 30) {
    errorMessage.value = '用户名长度需在 3-30 个字符内'
    return
  }

  // 仅允许中英文、数字、下划线和点，避免出现奇怪字符
  const usernamePattern = /^[\w.\u4e00-\u9fa5]+$/
  if (!usernamePattern.test(username)) {
    errorMessage.value = '用户名只能包含中英文、数字、下划线和点'
    return
  }

  if (nickname.length > 30) {
    errorMessage.value = '昵称长度不能超过 30 个字符'
    return
  }

  // 如果用户名、昵称都没变且没有选新头像，就不必发请求
  if (
    username === initialForm.username &&
    nickname === initialForm.nickname &&
    !avatarFile.value
  ) {
    errorMessage.value = '没有修改任何信息'
    return
  }

  saving.value = true
  errorMessage.value = ''
  
  try {
    const data = {
      username,
      nickname
    }
    
    if (avatarFile.value) {
      data.avatar = avatarFile.value
    }
    
    await authApi.updateUserInfo(data)
    const latest = await authStore.fetchUserInfo()
    if (latest) {
      user.value = latest
      initialForm.username = latest.username
      initialForm.nickname = latest.nickname
      // 如果上传了头像，清空预览（使用服务器返回的新头像）
      if (avatarFile.value) {
        avatarFile.value = null
        avatarPreview.value = ''
      }
    }
    
    showToast({
      message: '保存成功',
      type: 'success'
    })
    
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
  const newPhone = (phoneForm.new_phone || '').trim()
  if (!phoneForm.password || !newPhone) {
    phoneError.value = '请填写完整信息'
    return
  }
  
  if (!/^1\d{10}$/.test(newPhone)) {
    phoneError.value = '请输入正确的手机号'
    return
  }

  if (newPhone === currentPhone.value) {
    phoneError.value = '新手机号不能与当前手机号相同'
    return
  }
  
  changingPhone.value = true
  phoneError.value = ''
  
  try {
    await authApi.changePhone({
      password: phoneForm.password,
      new_phone: newPhone
    })
    const latest = await authStore.fetchUserInfo()
    if (latest) {
      user.value = latest
    }

    showToast({
      message: '手机号已更新',
      type: 'success'
    })
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
  background: $button-gradient;
  border-radius: $radius-full;
  font-size: $font-size-sm;
  font-weight: $font-weight-medium;
  color: $text-white;
  box-shadow: $shadow-sm;
  
  &:disabled {
    opacity: 0.5;
  }
}

.edit-section {
  margin-bottom: $spacing-lg;
}

.avatar-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $spacing-sm;
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
  color: $text-white;
}

.avatar-clear-btn {
  padding: 6px 16px;
  background: $glass-bg-heavy;
  backdrop-filter: $glass-blur;
  -webkit-backdrop-filter: $glass-blur;
  border: $glass-border;
  border-radius: $radius-full;
  font-size: $font-size-xs;
  color: $text-secondary;
  cursor: pointer;
  transition: all $transition-normal;
  
  &:hover {
    background: rgba(255, 255, 255, 0.9);
    color: $text-primary;
    transform: translateY(-1px);
  }
  
  &:active {
    transform: scale(0.95);
  }
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
  font-size: 18px;
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
  background: $glass-bg-heavy;
  border: $glass-border;
  border-radius: $radius-md;
  color: $text-primary;
  font-size: $font-size-base;
  
  &:focus {
    border-color: rgba($pink-primary, 0.5);
  }
}
</style>

