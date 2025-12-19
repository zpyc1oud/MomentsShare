<template>
  <PageLayout title="动态详情" :show-back="true" :show-tabbar="false">
    <div class="detail-page">
      <div v-if="loading" class="loading-container">
        <Loading text="加载中..." />
      </div>
      
      <template v-else-if="moment">
        <!-- 作者信息 -->
        <div class="author-section">
          <img :src="moment.author?.avatar || '/default-avatar.png'" class="avatar avatar--lg" />
          <div class="author-info">
            <span class="author-name">{{ moment.author?.nickname }}</span>
            <span class="author-time">{{ formatTime(moment.created_at) }}</span>
          </div>
        </div>
        
        <!-- 内容 -->
        <p v-if="moment.content" class="moment-content">{{ moment.content }}</p>
        
        <!-- 图片 -->
        <div v-if="moment.type === 'IMAGE' && moment.images?.length" class="moment-images">
          <img 
            v-for="(image, index) in moment.images" 
            :key="image.id"
            :src="image.image_file"
            class="moment-image"
            @click="previewImage(index)"
          />
        </div>
        
        <!-- 视频 -->
        <div v-if="moment.type === 'VIDEO' && moment.video_file" class="moment-video">
          <VideoPlayer :src="moment.video_file" />
        </div>
        
        <!-- 标签 -->
        <div v-if="moment.tags?.length" class="moment-tags">
          <span v-for="tag in moment.tags" :key="tag.id" class="tag"># {{ tag.name }}</span>
        </div>
        
        <div class="divider"></div>
        
        <!-- 评论区 -->
        <div class="comments-section">
          <h3 class="section-title">评论 ({{ comments.length }})</h3>
          
          <div class="comment-list">
            <div v-for="comment in comments" :key="comment.id" class="comment-item">
              <img :src="comment.author?.avatar || '/default-avatar.png'" class="avatar avatar--sm" />
              <div class="comment-body">
                <div class="comment-header">
                  <span class="comment-author">{{ comment.author?.nickname }}</span>
                  <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
                </div>
                <p class="comment-content">{{ comment.content }}</p>
                
                <!-- 回复 -->
                <div v-if="comment.replies?.length" class="reply-list">
                  <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
                    <span class="reply-author">{{ reply.author?.nickname }}</span>
                    <span class="reply-content">{{ reply.content }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="comments.length === 0" class="empty-comments">
            暂无评论，快来抢沙发吧~
          </div>
        </div>
      </template>
      
      <!-- 评论输入框 -->
      <div class="comment-input-bar">
        <input 
          v-model="commentText"
          type="text"
          class="comment-input"
          placeholder="写评论..."
          @keyup.enter="submitComment"
        />
        <button 
          class="send-btn"
          :disabled="!commentText.trim() || submitting"
          @click="submitComment"
        >
          发送
        </button>
      </div>
    </div>
    
    <!-- 图片预览 -->
    <ImagePreview 
      v-model="showPreview"
      :images="previewImages"
      :start-index="previewIndex"
    />
  </PageLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'
import PageLayout from '@/components/layout/PageLayout.vue'
import Loading from '@/components/common/Loading.vue'
import VideoPlayer from '@/components/common/VideoPlayer.vue'
import ImagePreview from '@/components/common/ImagePreview.vue'
import { momentsApi } from '@/api/moments'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

const route = useRoute()

const moment = ref(null)
const comments = ref([])
const loading = ref(true)
const commentText = ref('')
const submitting = ref(false)
const showPreview = ref(false)
const previewIndex = ref(0)

const previewImages = computed(() => {
  return moment.value?.images?.map(img => img.image_file) || []
})

const fetchMoment = async () => {
  try {
    const id = route.params.id
    const [momentRes, commentsRes] = await Promise.all([
      momentsApi.getDetail(id),
      momentsApi.getComments(id)
    ])
    
    moment.value = momentRes
    comments.value = commentsRes.results || []
  } catch (error) {
    console.error('Fetch moment error:', error)
  } finally {
    loading.value = false
  }
}

const formatTime = (time) => {
  return dayjs(time).fromNow()
}

const previewImage = (index) => {
  previewIndex.value = index
  showPreview.value = true
}

const submitComment = async () => {
  if (!commentText.value.trim() || submitting.value) return
  
  submitting.value = true
  
  try {
    const response = await momentsApi.createComment(route.params.id, {
      content: commentText.value
    })
    
    comments.value.unshift(response)
    commentText.value = ''
  } catch (error) {
    console.error('Submit comment error:', error)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchMoment()
})
</script>

<style lang="scss" scoped>
.detail-page {
  height: 100%;
  padding: $spacing-md;
  padding-bottom: 80px;
  overflow-y: auto;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: $spacing-xl;
}

.author-section {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  margin-bottom: $spacing-md;
}

.author-info {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-size: $font-size-lg;
  font-weight: $font-weight-semibold;
  color: $text-primary;
}

.author-time {
  font-size: $font-size-sm;
  color: $text-muted;
}

.moment-content {
  font-size: $font-size-base;
  line-height: 1.8;
  color: $text-primary;
  margin-bottom: $spacing-md;
}

.moment-images {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
  margin-bottom: $spacing-md;
}

.moment-image {
  width: 100%;
  border-radius: $radius-md;
  cursor: pointer;
}

.moment-video {
  border-radius: $radius-md;
  overflow: hidden;
  margin-bottom: $spacing-md;
}

.moment-tags {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-xs;
  margin-bottom: $spacing-md;
}

.comments-section {
  padding-top: $spacing-md;
}

.section-title {
  font-size: $font-size-base;
  font-weight: $font-weight-semibold;
  color: $text-primary;
  margin-bottom: $spacing-md;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
  padding-bottom: $spacing-lg;
}

.comment-item {
  display: flex;
  gap: $spacing-sm;
}

.comment-body {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  margin-bottom: 4px;
}

.comment-author {
  font-size: $font-size-sm;
  font-weight: $font-weight-medium;
  color: $text-primary;
}

.comment-time {
  font-size: $font-size-xs;
  color: $text-muted;
}

.comment-content {
  font-size: $font-size-sm;
  line-height: 1.5;
  color: $text-primary;
}

.reply-list {
  margin-top: $spacing-sm;
  padding: $spacing-sm;
  background: rgba($lavender, 0.1);
  border-radius: $radius-sm;
}

.reply-item {
  font-size: $font-size-sm;
  color: $text-secondary;
  
  & + & {
    margin-top: $spacing-xs;
  }
}

.reply-author {
  color: $pink-primary;
  margin-right: 4px;
}

.empty-comments {
  text-align: center;
  padding: $spacing-lg;
  color: $text-muted;
  font-size: $font-size-sm;
}

.comment-input-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 10;
  display: flex;
  gap: $spacing-sm;
  padding: $spacing-md;
  background: $glass-bg-heavy;
  backdrop-filter: $glass-blur;
  border-top: $glass-border-light;
}

.comment-input {
  flex: 1;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.8);
  border: $glass-border;
  border-radius: $radius-full;
  color: $text-primary;
  font-size: $font-size-sm;
  
  &:focus {
    border-color: rgba($pink-primary, 0.5);
  }
}

.send-btn {
  padding: 12px 20px;
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
</style>

