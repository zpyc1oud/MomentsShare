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
        <span class="content-count">{{ form.content.length }}/1000</span>
      </div>
      
      <!-- AI 润色按钮 -->
      <div class="ai-actions">
        <button class="ai-btn" @click="polishContent" :disabled="!form.content || polishing">
          <van-icon name="gem-o" /> {{ polishing ? 'AI润色中...' : 'AI润色' }}
        </button>
        <button class="ai-btn" @click="recommendTags" :disabled="!hasMedia || recommending">
          <van-icon name="label-o" /> {{ recommending ? '推荐中...' : '智能标签' }}
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
  </PageLayout>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import PageLayout from '@/components/layout/PageLayout.vue'
import { momentsApi } from '@/api/moments'
import { aiApi } from '@/api/ai'

const router = useRouter()

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

const hasMedia = computed(() => {
  return form.images.length > 0 || form.video
})

const canPublish = computed(() => {
  if (form.type === 'IMAGE') {
    return form.images.length > 0
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

const polishContent = async () => {
  if (!form.content) return
  
  polishing.value = true
  try {
    const response = await aiApi.polish({ text: form.content })
    if (response.generated_text) {
      form.content = response.generated_text
    }
  } catch (error) {
    console.error('Polish error:', error)
  } finally {
    polishing.value = false
  }
}

const recommendTags = async () => {
  if (!hasMedia.value) return
  
  recommending.value = true
  try {
    const data = { text: form.content }
    if (form.images.length > 0) {
      data.image = form.images[0]
    }
    
    const response = await aiApi.recommendTags(data)
    if (response.tags) {
      // 合并推荐标签（去重）
      response.tags.forEach(tag => {
        if (!form.labels.includes(tag) && form.labels.length < 5) {
          form.labels.push(tag)
        }
      })
    }
  } catch (error) {
    console.error('Recommend tags error:', error)
  } finally {
    recommending.value = false
  }
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
    alert(error.response?.data?.detail?.content?.[0] || '发布失败')
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
  position: absolute;
  right: $spacing-md;
  bottom: $spacing-md;
  font-size: $font-size-xs;
  color: $text-muted;
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
  
  &:hover:not(:disabled) {
    background: rgba($lavender, 0.25);
  }
  
  &:disabled {
    opacity: 0.5;
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
</style>

