<template>
  <div class="moment-card card card--hover" @click="$emit('click')">
    <!-- 作者信息 -->
    <div class="moment-header">
      <img :src="authorAvatar" :alt="moment.author?.nickname" class="avatar" />
      <div class="moment-author">
        <span class="moment-author__name">{{ moment.author?.nickname }}</span>
        <span class="moment-author__time">{{ formatTime(moment.created_at) }}</span>
      </div>
    </div>
    
    <!-- 内容 -->
    <p v-if="moment.content" class="moment-content text-clamp-2">
      {{ moment.content }}
    </p>
    
    <!-- 图片展示 -->
    <div v-if="moment.type === 'IMAGE' && moment.images?.length" class="moment-images" :class="imageGridClass">
      <div 
        v-for="(image, index) in displayImages" 
        :key="image.id"
        class="moment-image"
        @click.stop="previewImage(index)"
      >
        <img :src="image.image_file" :alt="`图片${index + 1}`" />
        <span v-if="index === 3 && moment.images.length > 4" class="image-more">
          +{{ moment.images.length - 4 }}
        </span>
      </div>
    </div>
    
    <!-- 视频展示 -->
    <div v-if="moment.type === 'VIDEO' && moment.video_file" class="moment-video">
      <VideoPlayer 
        :src="moment.video_file" 
        :show-controls="false"
        @click.stop
      />
    </div>
    
    <!-- 标签 -->
    <div v-if="moment.tags?.length" class="moment-tags">
      <span v-for="tag in moment.tags" :key="tag.id" class="tag">
        # {{ tag.name }}
      </span>
    </div>
    
    <!-- 互动栏 -->
    <div class="moment-actions">
      <button class="action-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
        </svg>
        <span>喜欢</span>
      </button>
      <button class="action-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/>
        </svg>
        <span>评论</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'
import VideoPlayer from '@/components/common/VideoPlayer.vue'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

const props = defineProps({
  moment: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])

const authorAvatar = computed(() => {
  return props.moment.author?.avatar || '/default-avatar.png'
})

const displayImages = computed(() => {
  return props.moment.images?.slice(0, 4) || []
})

const imageGridClass = computed(() => {
  const count = props.moment.images?.length || 0
  if (count === 1) return 'grid-1'
  if (count === 2) return 'grid-2'
  if (count === 3) return 'grid-3'
  return 'grid-4'
})

const formatTime = (time) => {
  return dayjs(time).fromNow()
}

const previewImage = (index) => {
  // TODO: 打开图片预览
  console.log('Preview image:', index)
}
</script>

<style lang="scss" scoped>
.moment-card {
  cursor: pointer;
}

.moment-header {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  margin-bottom: $spacing-sm;
}

.moment-author {
  display: flex;
  flex-direction: column;
  
  &__name {
    font-size: $font-size-base;
    font-weight: $font-weight-medium;
    color: $text-primary;
  }
  
  &__time {
    font-size: $font-size-xs;
    color: $text-muted;
  }
}

.moment-content {
  font-size: $font-size-base;
  line-height: 1.6;
  color: $text-primary;
  margin-bottom: $spacing-sm;
}

.moment-images {
  display: grid;
  gap: 4px;
  border-radius: $radius-md;
  overflow: hidden;
  margin-bottom: $spacing-sm;
  
  &.grid-1 {
    grid-template-columns: 1fr;
    
    .moment-image {
      aspect-ratio: 4/3;
    }
  }
  
  &.grid-2 {
    grid-template-columns: repeat(2, 1fr);
    
    .moment-image {
      aspect-ratio: 1;
    }
  }
  
  &.grid-3 {
    grid-template-columns: repeat(3, 1fr);
    
    .moment-image {
      aspect-ratio: 1;
    }
  }
  
  &.grid-4 {
    grid-template-columns: repeat(2, 1fr);
    
    .moment-image {
      aspect-ratio: 1;
    }
  }
}

.moment-image {
  position: relative;
  overflow: hidden;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .image-more {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: $font-size-xl;
    font-weight: $font-weight-bold;
    color: $text-primary;
  }
}

.moment-video {
  border-radius: $radius-md;
  overflow: hidden;
  margin-bottom: $spacing-sm;
  aspect-ratio: 16/9;
}

.moment-tags {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-xs;
  margin-bottom: $spacing-sm;
}

.moment-actions {
  display: flex;
  gap: $spacing-lg;
  padding-top: $spacing-sm;
  border-top: 1px solid $border-light;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  color: $text-muted;
  font-size: $font-size-sm;
  transition: color $transition-fast;
  
  svg {
    width: 18px;
    height: 18px;
  }
  
  &:hover {
    color: $primary-color;
  }
}
</style>

