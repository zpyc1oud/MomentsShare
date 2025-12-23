<template>
  <div 
    class="comment-item"
    :class="{ 
      'comment-item--selected': selectedId === comment.id,
      'comment-item--nested': depth > 0
    }"
    :style="{ marginLeft: depth > 0 ? '0' : undefined }"
    @click.stop="$emit('reply', comment)"
  >
    <img 
      :src="comment.author?.avatar || '/media/default_avatar.png'" 
      class="comment-avatar"
      :class="depth === 0 ? 'comment-avatar--md' : 'comment-avatar--sm'"
    />
    <div class="comment-body">
      <div class="comment-header">
        <span class="comment-author">{{ comment.author?.nickname }}</span>
        <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
      </div>
      <p class="comment-content">{{ comment.content }}</p>
      
      <!-- 递归渲染子评论 -->
      <div v-if="comment.replies?.length" class="replies-container">
        <CommentItem
          v-for="reply in comment.replies"
          :key="reply.id"
          :comment="reply"
          :depth="depth + 1"
          :selected-id="selectedId"
          @reply="$emit('reply', $event)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

defineProps({
  comment: {
    type: Object,
    required: true
  },
  depth: {
    type: Number,
    default: 0
  },
  selectedId: {
    type: Number,
    default: null
  }
})

defineEmits(['reply'])

const formatTime = (time) => {
  return dayjs(time).fromNow()
}
</script>

<style lang="scss" scoped>
.comment-item {
  display: flex;
  gap: $spacing-sm;
  padding: $spacing-sm;
  border-radius: $radius-sm;
  cursor: pointer;
  transition: background $transition-fast;
  
  &:hover {
    background: rgba($lavender, 0.08);
  }
  
  &--selected {
    background: rgba($pink-primary, 0.1) !important;
  }
  
  &--nested {
    margin-top: $spacing-xs;
    padding: $spacing-xs;
    
    &:hover {
      background: rgba($lavender, 0.12);
    }
  }
}

.comment-avatar {
  border-radius: 50%;
  flex-shrink: 0;
  object-fit: cover;
  
  &--md {
    width: 36px;
    height: 36px;
  }
  
  &--sm {
    width: 24px;
    height: 24px;
  }
}

.comment-body {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  margin-bottom: 2px;
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
  word-break: break-word;
}

.replies-container {
  margin-top: $spacing-xs;
  padding-left: $spacing-sm;
  border-left: 2px solid rgba($lavender, 0.3);
}
</style>
