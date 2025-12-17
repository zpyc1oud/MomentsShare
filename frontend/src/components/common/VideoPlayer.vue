<template>
  <div class="video-player" :class="{ 'video-player--playing': isPlaying }">
    <video
      ref="videoRef"
      :src="src"
      :poster="poster"
      class="video-player__video"
      playsinline
      @play="isPlaying = true"
      @pause="isPlaying = false"
      @ended="isPlaying = false"
      @timeupdate="onTimeUpdate"
      @loadedmetadata="onLoadedMetadata"
    ></video>
    
    <!-- 播放/暂停按钮覆盖层 -->
    <div class="video-player__overlay" @click="togglePlay">
      <transition name="fade">
        <div v-if="!isPlaying" class="video-player__play-btn">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M8 5v14l11-7z"/>
          </svg>
        </div>
      </transition>
    </div>
    
    <!-- 控制栏 -->
    <div class="video-player__controls" v-if="showControls">
      <button class="control-btn" @click="togglePlay">
        <svg v-if="isPlaying" viewBox="0 0 24 24" fill="currentColor">
          <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="currentColor">
          <path d="M8 5v14l11-7z"/>
        </svg>
      </button>
      
      <div class="progress-bar" @click="seek">
        <div class="progress-bar__track">
          <div class="progress-bar__fill" :style="{ width: progress + '%' }"></div>
        </div>
      </div>
      
      <span class="time-display">
        {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
      </span>
      
      <button class="control-btn" @click="toggleFullscreen">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M8 3H5a2 2 0 00-2 2v3m18 0V5a2 2 0 00-2-2h-3m0 18h3a2 2 0 002-2v-3M3 16v3a2 2 0 002 2h3"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  src: {
    type: String,
    required: true
  },
  poster: {
    type: String,
    default: ''
  },
  showControls: {
    type: Boolean,
    default: true
  }
})

const videoRef = ref(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const progress = ref(0)

const togglePlay = () => {
  if (!videoRef.value) return
  
  if (isPlaying.value) {
    videoRef.value.pause()
  } else {
    videoRef.value.play()
  }
}

const onTimeUpdate = () => {
  if (!videoRef.value) return
  currentTime.value = videoRef.value.currentTime
  progress.value = (currentTime.value / duration.value) * 100
}

const onLoadedMetadata = () => {
  if (!videoRef.value) return
  duration.value = videoRef.value.duration
}

const seek = (e) => {
  if (!videoRef.value) return
  const rect = e.currentTarget.getBoundingClientRect()
  const percent = (e.clientX - rect.left) / rect.width
  videoRef.value.currentTime = percent * duration.value
}

const toggleFullscreen = () => {
  if (!videoRef.value) return
  
  if (document.fullscreenElement) {
    document.exitFullscreen()
  } else {
    videoRef.value.requestFullscreen()
  }
}

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

defineExpose({
  play: () => videoRef.value?.play(),
  pause: () => videoRef.value?.pause()
})
</script>

<style lang="scss" scoped>
.video-player {
  position: relative;
  width: 100%;
  background: #000;
  border-radius: $radius-md;
  overflow: hidden;
  
  &__video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
  
  &__overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  
  &__play-btn {
    width: 60px;
    height: 60px;
    background: rgba(0, 0, 0, 0.6);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    
    svg {
      width: 28px;
      height: 28px;
      margin-left: 4px;
    }
  }
  
  &__controls {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    padding: $spacing-sm $spacing-md;
    background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  }
  
  &--playing {
    .video-player__controls {
      opacity: 0;
      transition: opacity 0.3s;
    }
    
    &:hover .video-player__controls {
      opacity: 1;
    }
  }
}

.control-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  
  svg {
    width: 18px;
    height: 18px;
  }
}

.progress-bar {
  flex: 1;
  height: 24px;
  display: flex;
  align-items: center;
  cursor: pointer;
  
  &__track {
    width: 100%;
    height: 4px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 2px;
    overflow: hidden;
  }
  
  &__fill {
    height: 100%;
    background: $pink-primary;
    border-radius: 2px;
    transition: width 0.1s linear;
  }
}

.time-display {
  font-size: $font-size-xs;
  color: $text-secondary;
  flex-shrink: 0;
}
</style>

