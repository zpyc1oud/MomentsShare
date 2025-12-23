<template>
  <PageLayout title="动态详情" :show-back="true" :show-tabbar="false">
    <div class="detail-page">
      <div v-if="loading" class="loading-container">
        <Loading text="加载中..." />
      </div>
      
      <template v-else-if="moment">
        <!-- 作者信息 -->
        <div class="author-section">
          <img :src="moment.author?.avatar || '/media/default_avatar.png'" class="avatar avatar--lg" />
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

        <!-- 点赞和统计信息 -->
        <div class="moment-stats">
          <button
            class="like-btn"
            :class="{ 'like-btn--liked': moment.is_liked }"
            @click="handleLike"
          >
            <svg viewBox="0 0 24 24" :fill="moment.is_liked ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
              <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
            </svg>
            <span>{{ moment.likes_count || 0 }} 赞</span>
          </button>
        </div>

        <div class="divider"></div>
        
        <!-- 评论区 -->
        <div class="comments-section">
          <h3 class="section-title">评论 ({{ comments.length }})</h3>
          
          <div class="comment-list">
            <CommentItem
              v-for="comment in comments"
              :key="comment.id"
              :comment="comment"
              :depth="0"
              :selected-id="replyingTo?.id"
              @reply="startReply"
            />
          </div>
          
          <div v-if="comments.length === 0" class="empty-comments">
            暂无评论，快来抢沙发吧~
          </div>
        </div>
      </template>
      
      <!-- 评论输入框 -->
      <div class="comment-input-bar">
        <div v-if="replyingTo" class="replying-hint">
          <span>回复 @{{ replyingTo.author?.nickname }}</span>
          <button class="cancel-reply" @click="cancelReply">×</button>
        </div>
        <div class="input-row">
          <input 
            ref="commentInputRef"
            v-model="commentText"
            type="text"
            class="comment-input"
            :placeholder="replyingTo ? `回复 ${replyingTo.author?.nickname}...` : '写评论...'"
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
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'
import PageLayout from '@/components/layout/PageLayout.vue'
import Loading from '@/components/common/Loading.vue'
import VideoPlayer from '@/components/common/VideoPlayer.vue'
import ImagePreview from '@/components/common/ImagePreview.vue'
import CommentItem from '@/components/business/CommentItem.vue'
import { momentsApi } from '@/api/moments'
import { showToast } from 'vant'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

const route = useRoute()

const moment = ref(null)
const comments = ref([])
const loading = ref(true)
const commentText = ref('')
const submitting = ref(false)
const replyingTo = ref(null)
const commentInputRef = ref(null)
const showPreview = ref(false)
const previewIndex = ref(0)
const likeLoading = ref(false)

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

// 递归查找评论
const findCommentById = (commentsList, targetId) => {
  for (const comment of commentsList) {
    if (comment.id === targetId) {
      return comment
    }
    if (comment.replies?.length) {
      const found = findCommentById(comment.replies, targetId)
      if (found) return found
    }
  }
  return null
}

const submitComment = async () => {
  if (!commentText.value.trim() || submitting.value) return
  
  submitting.value = true
  
  try {
    const data = { content: commentText.value }
    
    // 如果是回复评论，添加parent_id
    if (replyingTo.value) {
      data.parent_id = replyingTo.value.id
    }
    
    const response = await momentsApi.createComment(route.params.id, data)
    
    if (replyingTo.value) {
      // 楼中楼回复，递归查找父评论并添加到replies中
      const parentComment = findCommentById(comments.value, replyingTo.value.id)
      if (parentComment) {
        if (!parentComment.replies) {
          parentComment.replies = []
        }
        parentComment.replies.push(response)
      }
    } else {
      // 顶级评论
      comments.value.unshift(response)
    }
    
    commentText.value = ''
    replyingTo.value = null
  } catch (error) {
    console.error('Submit comment error:', error)
    showToast({
      message: error.response?.data?.detail || '评论失败',
      type: 'fail'
    })
  } finally {
    submitting.value = false
  }
}

// 开始回复评论
const startReply = (comment) => {
  replyingTo.value = comment
  // 聚焦输入框
  nextTick(() => {
    commentInputRef.value?.focus()
  })
}

// 取消回复
const cancelReply = () => {
  replyingTo.value = null
}

// 处理点赞
const handleLike = async () => {
  if (likeLoading.value || !moment.value) return

  likeLoading.value = true

  try {
    const response = await momentsApi.toggleLike(moment.value.id)

    // 更新点赞状态和数量
    moment.value.is_liked = response.liked
    moment.value.likes_count = response.likes_count

    showToast({
      message: response.detail,
      type: 'success',
      position: 'bottom'
    })
  } catch (error) {
    console.error('Like error:', error)
    showToast({
      message: error.response?.data?.detail || '操作失败',
      type: 'fail',
      position: 'bottom'
    })
  } finally {
    likeLoading.value = false
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

.moment-stats {
  padding: $spacing-md 0;
  display: flex;
  align-items: center;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba($lavender, 0.1);
  border: 1px solid rgba($lavender, 0.2);
  border-radius: $radius-full;
  color: $text-secondary;
  font-size: $font-size-sm;
  transition: all $transition-normal;
  cursor: pointer;

  svg {
    width: 20px;
    height: 20px;
  }

  &:hover {
    background: rgba($lavender, 0.15);
    border-color: rgba($lavender, 0.3);
  }

  &:active {
    transform: scale(0.95);
  }

  &--liked {
    background: rgba($pink-primary, 0.15);
    border-color: $pink-primary;
    color: $pink-primary;

    &:hover {
      background: rgba($pink-primary, 0.2);
    }
  }
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
  gap: $spacing-xs;
  padding-bottom: $spacing-lg;
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
  flex-direction: column;
  gap: $spacing-xs;
  padding: $spacing-md;
  background: $glass-bg-heavy;
  backdrop-filter: $glass-blur;
  border-top: $glass-border-light;
}

.replying-hint {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 12px;
  background: rgba($pink-primary, 0.1);
  border-radius: $radius-sm;
  font-size: $font-size-xs;
  color: $pink-primary;
}

.cancel-reply {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  font-size: 16px;
  color: $text-muted;
  cursor: pointer;
  
  &:hover {
    color: $text-primary;
  }
}

.input-row {
  display: flex;
  gap: $spacing-sm;
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

