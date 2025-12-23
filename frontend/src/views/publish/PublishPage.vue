<template>
  <PageLayout title="发布动态" :show-back="true" :show-tabbar="false">
    <template #nav-right>
      <button 
        class="publish-btn" 
        :disabled="!canPublish || publishing"
        @click="handlePublish"
      >
        {{ publishing ? '发布中...' : '发布' }}
      </button>
    </template>
    
    <div class="publish-page">
      <!-- 内容输入 -->
      <div class="content-section">
        <textarea
          v-model="form.content"
          class="content-input"
          placeholder="分享你的生活点滴..."
          maxlength="1000"
        ></textarea>
        <div class="content-footer">
          <button class="model-selector-btn" @click="showModelSelector = !showModelSelector">
            <img :src="selectedModel.icon" class="model-icon" alt="model icon" />
            <span class="model-name">{{ selectedModel.name }}</span>
            <van-icon name="arrow-down" :class="{ 'rotate': showModelSelector }" />
          </button>
          <span class="content-count">{{ form.content.length }}/1000</span>
        </div>

        <!-- 模型选择器弹窗 -->
        <div v-if="showModelSelector" class="model-selector">
          <div
            v-for="(model, index) in aiModels"
            :key="model.id"
            class="model-option"
            :class="{ active: selectedModelIndex === index }"
            @click="selectModel(index)"
          >
            <img :src="model.icon" class="model-icon" alt="model icon" />
            <span class="model-name">{{ model.name }}</span>
            <van-icon v-if="selectedModelIndex === index" name="success" />
          </div>
        </div>
      </div>
      
      <!-- AI 润色按钮 -->
      <div class="ai-actions">
        <button
          class="ai-btn"
          :class="{ 'ai-btn--disabled': !form.content.trim() }"
          @click="polishContent"
          :disabled="polishing"
        >
          <van-icon name="gem-o" />
          <img :src="selectedModel.icon" class="btn-model-icon" alt="model icon" />
          {{ polishing ? 'AI润色中...' : 'AI润色' }}
        </button>
        <button
          class="ai-btn"
          :class="{ 'ai-btn--disabled': !hasMedia }"
          @click="recommendTags"
          :disabled="recommending"
        >
          <van-icon name="label-o" />
          <img :src="selectedModel.icon" class="btn-model-icon" alt="model icon" />
          {{ recommending ? '推荐中...' : '智能标签' }}
        </button>
      </div>
      
      <!-- 媒体选择 -->
      <div class="media-section">
        <div class="media-tabs">
          <button 
            class="media-tab" 
            :class="{ active: form.type === 'IMAGE' }"
            @click="switchType('IMAGE')"
          >
            <van-icon name="photo-o" /> 图片
          </button>
          <button 
            class="media-tab" 
            :class="{ active: form.type === 'VIDEO' }"
            @click="switchType('VIDEO')"
          >
            <van-icon name="video-o" /> 视频
          </button>
        </div>
        
        <!-- 图片上传 -->
        <div v-if="form.type === 'IMAGE'" class="image-upload">
          <div class="image-grid">
            <div 
              v-for="(image, index) in imagePreview" 
              :key="index"
              class="image-item"
            >
              <img :src="image" alt="预览图" />
              <button class="remove-btn" @click="removeImage(index)">
                <van-icon name="cross" />
              </button>
            </div>
            <label v-if="imagePreview.length < 9" class="upload-trigger">
              <input 
                type="file"
                accept="image/*"
                multiple
                hidden
                @change="handleImageSelect"
              />
              <van-icon name="plus" class="upload-icon" />
              <span class="upload-text">添加图片</span>
            </label>
          </div>
          <p class="upload-tip">最多可上传9张图片</p>
        </div>
        
        <!-- 视频上传 -->
        <div v-else class="video-upload">
          <div v-if="videoPreview" class="video-preview">
            <video :src="videoPreview" controls></video>
            <button class="remove-btn" @click="removeVideo">
              <van-icon name="cross" />
            </button>
          </div>
          <label v-else class="upload-trigger upload-trigger--video">
            <input 
              type="file"
              accept="video/*"
              hidden
              @change="handleVideoSelect"
            />
            <van-icon name="video-o" class="upload-icon" />
            <span class="upload-text">选择视频</span>
          </label>
        </div>
      </div>

      <!-- 标签输入 -->
      <div class="tags-section">
        <h4 class="section-title">添加标签</h4>
        <div class="tags-input">
          <div class="tag-list">
            <span v-for="(tag, index) in form.labels" :key="index" class="tag">
              # {{ tag }}
              <button @click="removeTag(index)">×</button>
            </span>
          </div>
          <input
            v-model="newTag"
            type="text"
            class="tag-input"
            placeholder="输入标签，回车添加"
            maxlength="10"
            @keyup.enter="addTag"
          />
        </div>
      </div>
    </div>

    <!-- 自定义提示框 -->
    <Transition name="toast-fade">
      <div v-if="customToast.show" class="custom-toast" :class="`custom-toast--${customToast.type}`">
        <div class="toast-icon">
          <!-- 渐变警告图标 - 使用SVG实现渐变填充 -->
          <svg v-if="customToast.type === 'warning'" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" class="gradient-icon">
            <defs>
              <linearGradient id="warningGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#FCAEC1;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#B7A8D6;stop-opacity:1" />
              </linearGradient>
            </defs>
            <path fill="url(#warningGradient)" d="M512 85.333333c235.648 0 426.666667 191.018667 426.666667 426.666667s-191.018667 426.666667-426.666667 426.666667S85.333333 747.648 85.333333 512 276.351667 85.333333 512 85.333333z m0 64C306.816 149.333333 149.333333 306.816 149.333333 512s157.482667 362.666667 362.666667 362.666667 362.666667-157.482667 362.666667-362.666667S717.184 149.333333 512 149.333333z m0 586.666667c-23.573333 0-42.666667-19.093333-42.666667-42.666667s19.093333-42.666667 42.666667-42.666667 42.666667 19.093333 42.666667 42.666667-19.093333 42.666667-42.666667 42.666667z m0-512c23.573333 0 42.666667 19.093333 42.666667 42.666667v298.666667c0 23.573333-19.093333 42.666667-42.666667 42.666667s-42.666667-19.093333-42.666667-42.666667V266.666667c0-23.573333 19.093333-42.666667 42.666667-42.666667z"/>
          </svg>
          <!-- 成功和错误图标继续使用Vant -->
          <van-icon v-else-if="customToast.type === 'success'" name="checked" />
          <van-icon v-else-if="customToast.type === 'error'" name="close" />
        </div>
        <span class="toast-message">{{ customToast.message }}</span>
      </div>
    </Transition>
  </PageLayout>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import PageLayout from '@/components/layout/PageLayout.vue'
import { momentsApi } from '@/api/moments'
import { aiApi } from '@/api/ai'

const router = useRouter()

// AI 模型配置（可扩展）
const aiModels = [
  { id: 'Qwen/Qwen2.5-7B-Instruct', name: '通义千问 Qwen2.5', icon: '/image/qwen_icon.png', iconType: 'image' },
  { id: 'Qwen/Qwen3-VL-8B-Instruct', name: '通义千问 VL', icon: '/image/qwen_icon.png', iconType: 'image' },
  { id: 'zai-org/GLM-4.6V', name: '智谱 GLM-4.6V', icon: '/image/zai_icon.png', iconType: 'image' },
  { id: 'stepfun-ai/step3', name: '阶跃星辰 s3', icon: '/image/Stepfun_icon.png', iconType: 'image' }
]

const form = reactive({
  content: '',
  type: 'IMAGE',
  images: [],
  video: null,
  labels: []
})

const imagePreview = ref([])
const videoPreview = ref('')
const newTag = ref('')
const publishing = ref(false)
const polishing = ref(false)
const recommending = ref(false)
const selectedModelIndex = ref(0) // 默认选择第一个模型
const showModelSelector = ref(false) // 模型选择器显示状态

// 自定义提示框状态
const customToast = reactive({
  show: false,
  message: '',
  type: 'warning', // warning, success, error
  timer: null
})

// 显示自定义提示
const showCustomToast = (message, type = 'warning', duration = 1000) => {
  if (customToast.timer) {
    clearTimeout(customToast.timer)
  }

  customToast.message = message
  customToast.type = type
  customToast.show = true

  customToast.timer = setTimeout(() => {
    customToast.show = false
  }, duration)
}

const selectedModel = computed(() => aiModels[selectedModelIndex.value])

const hasMedia = computed(() => {
  return form.images.length > 0 || form.video
})

const canPublish = computed(() => {
  if (form.type === 'IMAGE') {
    // 允许纯文字或带图片
    return form.content.trim().length > 0 || form.images.length > 0
  }
  return !!form.video
})

const switchType = (type) => {
  form.type = type
  // 清空另一种类型的媒体
  if (type === 'IMAGE') {
    form.video = null
    videoPreview.value = ''
  } else {
    form.images = []
    imagePreview.value = []
  }
}

const handleImageSelect = (e) => {
  const files = Array.from(e.target.files)
  const remaining = 9 - form.images.length
  const toAdd = files.slice(0, remaining)
  
  toAdd.forEach(file => {
    form.images.push(file)
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value.push(e.target.result)
    }
    reader.readAsDataURL(file)
  })
  
  e.target.value = ''
}

const removeImage = (index) => {
  form.images.splice(index, 1)
  imagePreview.value.splice(index, 1)
}

const handleVideoSelect = (e) => {
  const file = e.target.files[0]
  if (file) {
    form.video = file
    videoPreview.value = URL.createObjectURL(file)
  }
}

const removeVideo = () => {
  form.video = null
  videoPreview.value = ''
}

const addTag = () => {
  const tag = newTag.value.trim()
  if (tag && !form.labels.includes(tag) && form.labels.length < 5) {
    form.labels.push(tag)
    newTag.value = ''
  }
}

const removeTag = (index) => {
  form.labels.splice(index, 1)
}

/**
 * 从视频文件中截取首帧作为图片
 * @param {File} videoFile - 视频文件
 * @returns {Promise<File>} - 返回截图后的图片文件
 */
const captureVideoFrame = async (videoFile) => {
  return new Promise((resolve, reject) => {
    const video = document.createElement('video')
    video.preload = 'metadata'
    video.muted = true // 静音以避免自动播放策略限制

    video.onloadedmetadata = () => {
      // 跳转到视频开始位置
      video.currentTime = 0
    }

    video.onseeked = () => {
      try {
        // 创建 canvas 来截取视频帧
        const canvas = document.createElement('canvas')
        canvas.width = video.videoWidth
        canvas.height = video.videoHeight

        const ctx = canvas.getContext('2d')
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

        // 将 canvas 转换为 blob
        canvas.toBlob((blob) => {
          if (blob) {
            // 创建 File 对象
            const frameFile = new File([blob], 'video_frame.jpg', {
              type: 'image/jpeg',
              lastModified: Date.now()
            })
            resolve(frameFile)
          } else {
            reject(new Error('Failed to capture video frame'))
          }
        }, 'image/jpeg', 0.9)
      } catch (error) {
        reject(error)
      } finally {
        // 清理视频对象
        URL.revokeObjectURL(video.src)
      }
    }

    video.onerror = () => {
      reject(new Error('Failed to load video'))
      URL.revokeObjectURL(video.src)
    }

    // 设置视频源
    video.src = URL.createObjectURL(videoFile)
  })
}

const polishContent = async () => {
  if (!form.content.trim()) {
    showCustomToast('请先输入文本哦', 'warning')
    return
  }

  // GLM 模型可能需要更长时间，显示提示
  if (selectedModel.value.id.includes('GLM')) {
    showToast({
      message: 'GLM 模型响应较慢，请耐心等待...',
      duration: 3000
    })
  }

  polishing.value = true
  try {
    const response = await aiApi.polish({
      text: form.content,
      model: selectedModel.value.id
    })
    if (response.polished_content) {
      form.content = response.polished_content

      // 同时显示推荐的标签给用户
      if (response.suggested_tags && response.suggested_tags.length > 0) {
        console.log('AI推荐的标签:', response.suggested_tags)
      }

      showToast({
        message: 'AI润色完成！',
        type: 'success'
      })
    }
  } catch (error) {
    console.error('Polish error:', error)
    // 修复 Toast message 类型问题
    let errorMessage = 'AI润色失败，请重试'
    if (error.response?.data) {
      const detail = error.response.data.detail
      errorMessage = typeof detail === 'string' ? detail : JSON.stringify(detail)
    } else if (error.message) {
      errorMessage = error.message
    }

    showToast({
      message: errorMessage,
      type: 'fail'
    })
  } finally {
    polishing.value = false
  }
}

const recommendTags = async () => {
  if (!hasMedia.value) {
    showCustomToast('请先上传视频或图片哦', 'warning')
    return
  }

  // GLM 模型可能需要更长时间，显示提示
  if (selectedModel.value.id.includes('GLM')) {
    showToast({
      message: 'GLM 模型响应较慢，请耐心等待...',
      duration: 3000
    })
  }

  // 如果是视频模式，显示处理中提示
  if (form.type === 'VIDEO' && form.video) {
    showToast({
      message: '正在截取视频首帧...',
      duration: 2000
    })
  }

  recommending.value = true
  try {
    const data = {
      text: form.content || '', // 确保即使为空也传递空字符串
      model: selectedModel.value.id
    }

    // 如果是图片模式且有图片，直接使用图片
    if (form.type === 'IMAGE' && form.images.length > 0) {
      data.image = form.images[0]
    }
    // 如果是视频模式，截取视频首帧
    else if (form.type === 'VIDEO' && form.video) {
      try {
        showToast({
          message: '正在分析视频内容...',
          duration: 2000
        })
        const videoFrame = await captureVideoFrame(form.video)
        data.image = videoFrame
      } catch (error) {
        console.error('Failed to capture video frame:', error)
        showToast({
          message: '视频处理失败，请上传图片或添加文字描述',
          type: 'fail'
        })
        return
      }
    }

    const response = await aiApi.recommendTags(data)
    if (response.tags) {
      // 合并推荐标签（去重）
      const addedTags = []
      response.tags.forEach(tag => {
        if (!form.labels.includes(tag) && form.labels.length < 5) {
          form.labels.push(tag)
          addedTags.push(tag)
        }
      })

      if (addedTags.length > 0) {
        showToast({
          message: `已添加 ${addedTags.length} 个标签`,
          type: 'success'
        })
      } else {
        showToast({
          message: '标签已存在或已达上限',
          type: 'warning'
        })
      }
    }
  } catch (error) {
    console.error('Recommend tags error:', error)
    // 修复 Toast message 类型问题
    let errorMessage = '标签推荐失败，请重试'
    if (error.response?.data) {
      const detail = error.response.data.detail
      errorMessage = typeof detail === 'string' ? detail : JSON.stringify(detail)
    } else if (error.message) {
      errorMessage = error.message
    }

    showToast({
      message: errorMessage,
      type: 'fail'
    })
  } finally {
    recommending.value = false
  }
}

const selectModel = (index) => {
  selectedModelIndex.value = index
  showModelSelector.value = false
}

const handlePublish = async () => {
  if (!canPublish.value) return

  publishing.value = true

  try {
    await momentsApi.create({
      content: form.content,
      type: form.type,
      images: form.type === 'IMAGE' ? form.images : [],
      video: form.type === 'VIDEO' ? form.video : null,
      labels: form.labels
    })

    router.push('/home')
  } catch (error) {
    console.error('Publish error:', error)
    // 提取错误消息，处理可能的敏感词错误
    let errorMessage = '发布失败，请重试'

    if (error.response?.data) {
      const detail = error.response.data.detail

      // 检查是否是敏感词错误
      if (detail?.content) {
        // 内容敏感词错误
        if (Array.isArray(detail.content)) {
          errorMessage = detail.content[0] || errorMessage
        } else {
          errorMessage = detail.content
        }
      } else if (detail?.labels) {
        // 标签敏感词错误
        if (Array.isArray(detail.labels)) {
          errorMessage = detail.labels[0] || errorMessage
        } else {
          errorMessage = detail.labels
        }
      } else if (typeof detail === 'string') {
        errorMessage = detail
      } else if (detail?.message) {
        errorMessage = detail.message
      }
    }

    // 使用自定义提示框显示错误
    showCustomToast(errorMessage, 'warning')
  } finally {
    publishing.value = false
  }
}
</script>

<style lang="scss" scoped>
.publish-page {
  padding: $spacing-md;
}

.publish-btn {
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

.content-section {
  position: relative;
  margin-bottom: $spacing-md;
}

.content-input {
  width: 100%;
  min-height: 150px;
  padding: $spacing-md;
  background: $glass-bg-heavy;
  backdrop-filter: $glass-blur;
  border: $glass-border;
  border-radius: $radius-md;
  color: $text-primary;
  font-size: $font-size-base;
  line-height: 1.6;
  resize: none;
  
  &:focus {
    border-color: rgba($pink-primary, 0.5);
  }
  
  &::placeholder {
    color: $text-placeholder;
  }
}

.content-count {
  font-size: $font-size-xs;
  color: $text-muted;
}

.content-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 $spacing-md $spacing-md $spacing-md;
}

.model-selector-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba($lavender, 0.1);
  border: 1px solid rgba($lavender, 0.3);
  border-radius: $radius-full;
  font-size: $font-size-xs;
  color: $lavender;
  transition: all $transition-fast;
  cursor: pointer;

  &:hover {
    background: rgba($lavender, 0.2);
  }

  .model-icon {
    width: 14px;
    height: 14px;
    object-fit: contain;
  }

  .model-name {
    max-width: 120px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .van-icon {
    font-size: 12px;
    transition: transform $transition-fast;

    &.rotate {
      transform: rotate(180deg);
    }
  }
}

.model-selector {
  position: absolute;
  left: $spacing-md;
  right: $spacing-md;
  bottom: 50px;
  background: $glass-bg-heavy;
  backdrop-filter: $glass-blur;
  border: $glass-border;
  border-radius: $radius-md;
  padding: $spacing-xs;
  box-shadow: $shadow-lg;
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
}

.model-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: $radius-sm;
  cursor: pointer;
  transition: all $transition-fast;

  &:hover {
    background: rgba($lavender, 0.1);
  }

  &.active {
    background: rgba($pink-primary, 0.15);
  }

  .model-icon {
    width: 18px;
    height: 18px;
    object-fit: contain;
  }

  .model-name {
    flex: 1;
    font-size: $font-size-sm;
    color: $text-primary;
  }

  .van-icon {
    color: $pink-primary;
    font-size: 16px;
  }
}

.ai-actions {
  display: flex;
  gap: $spacing-sm;
  margin-bottom: $spacing-lg;
}

.ai-btn {
  flex: 1;
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: rgba($lavender, 0.15);
  border: 1px solid rgba($lavender, 0.3);
  border-radius: $radius-md;
  font-size: $font-size-sm;
  color: $lavender;
  transition: all $transition-fast;

  &:hover:not(:disabled):not(.ai-btn--disabled) {
    background: rgba($lavender, 0.25);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  // 自定义禁用状态（允许点击但显示灰色）
  &.ai-btn--disabled {
    opacity: 0.5;
    cursor: pointer;
  }

  .btn-model-icon {
    width: 14px;
    height: 14px;
    object-fit: contain;
  }
}

.media-section {
  margin-bottom: $spacing-lg;
}

.media-tabs {
  display: flex;
  gap: $spacing-sm;
  margin-bottom: $spacing-md;
}

.media-tab {
  flex: 1;
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: $glass-bg;
  backdrop-filter: $glass-blur;
  border: $glass-border;
  border-radius: $radius-md;
  font-size: $font-size-sm;
  color: $text-secondary;
  transition: all $transition-fast;
  
  &.active {
    background: rgba($pink-primary, 0.15);
    border-color: $pink-primary;
    color: $pink-primary;
  }
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-sm;
}

.image-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: $radius-md;
  overflow: hidden;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .remove-btn {
    position: absolute;
    top: 4px;
    right: 4px;
    width: 24px;
    height: 24px;
    background: rgba(0, 0, 0, 0.6);
    border-radius: 50%;
    color: white;
    font-size: 16px;
    line-height: 1;
  }
}

.upload-trigger {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: $glass-bg;
  border: 2px dashed rgba($lavender, 0.4);
  border-radius: $radius-md;
  cursor: pointer;
  transition: all $transition-fast;
  
  &:hover {
    border-color: $pink-primary;
    background: rgba($pink-primary, 0.05);
  }
  
  .upload-icon {
    font-size: 24px;
    color: $text-muted;
  }
  
  .upload-text {
    font-size: $font-size-xs;
    color: $text-muted;
    margin-top: 4px;
  }
  
  &--video {
    aspect-ratio: 16/9;
  }
}

.upload-tip {
  font-size: $font-size-xs;
  color: $text-muted;
  margin-top: $spacing-sm;
  text-align: center;
}

.video-preview {
  position: relative;
  border-radius: $radius-md;
  overflow: hidden;
  
  video {
    width: 100%;
    aspect-ratio: 16/9;
    object-fit: cover;
  }
  
  .remove-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 32px;
    height: 32px;
    background: rgba(0, 0, 0, 0.6);
    border-radius: 50%;
    color: white;
    font-size: 20px;
  }
}

.tags-section {
  margin-bottom: $spacing-lg;
}

.section-title {
  font-size: $font-size-sm;
  font-weight: $font-weight-medium;
  color: $text-secondary;
  margin-bottom: $spacing-sm;
}

.tags-input {
  background: $glass-bg-heavy;
  backdrop-filter: $glass-blur;
  border: $glass-border;
  border-radius: $radius-md;
  padding: $spacing-sm;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-xs;
  margin-bottom: $spacing-xs;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: rgba($lavender, 0.2);
  border-radius: $radius-full;
  font-size: $font-size-sm;
  color: $lavender;
  
  button {
    font-size: 14px;
    opacity: 0.7;
    
    &:hover {
      opacity: 1;
    }
  }
}

.tag-input {
  width: 100%;
  padding: 8px 0;
  background: transparent;
  font-size: $font-size-sm;

  &::placeholder {
    color: $text-placeholder;
  }
}

// 自定义提示框样式
.custom-toast {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  min-width: auto;
  max-width: 90%;
  width: fit-content;
  padding: 12px 18px;
  display: flex;
  align-items: center;
  gap: 10px;
  background: $glass-bg-heavy;
  backdrop-filter: $glass-blur;
  border: $glass-border;
  border-radius: $radius-md;
  box-shadow: $shadow-lg, $shadow-glow;
  z-index: 9999;

  // 提示类型样式
  &--warning {
    .toast-icon {
      animation: icon-bounce 0.5s ease-out;

      .gradient-icon {
        width: 20px;
        height: 20px;
        display: block;
      }
    }
  }

  &--success {
    .toast-icon {
      color: $success-color;
      animation: icon-check 0.5s ease-out;
    }
  }

  &--error {
    .toast-icon {
      color: $error-color;
      animation: icon-shake 0.5s ease-out;
    }
  }

  .toast-icon {
    font-size: 20px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .toast-message {
    flex: 1;
    font-size: $font-size-sm;
    color: $text-primary;
    line-height: 1.4;
    font-weight: $font-weight-medium;
    white-space: nowrap;
  }
}

// 提示框动画
.toast-fade-enter-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.toast-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 1, 1);
}

.toast-fade-enter-from {
  opacity: 0;
  transform: translate(-50%, -45%) scale(0.9);
}

.toast-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -55%) scale(0.95);
}

// 图标动画
@keyframes icon-bounce {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes icon-check {
  0% {
    transform: scale(0) rotate(-180deg);
    opacity: 0;
  }
  50% {
    transform: scale(1.1) rotate(10deg);
  }
  100% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
}

@keyframes icon-shake {
  0%, 100% {
    transform: translateX(0);
    opacity: 1;
  }
  10%, 30%, 50%, 70%, 90% {
    transform: translateX(-4px);
  }
  20%, 40%, 60%, 80% {
    transform: translateX(4px);
  }
  50% {
    opacity: 0;
  }
  55% {
    opacity: 1;
  }
}
</style>

