<template>
  <div 
    class="page-layout" 
    :class="{ 
      'has-navbar': showNavbar, 
      'has-tabbar': showTabbar,
      'nav-transparent': navTransparent 
    }"
  >
    <!-- 导航栏 -->
    <NavBar 
      v-if="showNavbar"
      :title="title"
      :show-back="showBack"
      :transparent="navTransparent"
      @back="handleBack"
    >
      <template v-if="$slots['nav-left']" #left>
        <slot name="nav-left"></slot>
      </template>
      <template v-if="$slots['nav-right']" #right>
        <slot name="nav-right"></slot>
      </template>
    </NavBar>
    
    <!-- 页面内容 -->
    <div 
      class="page-content"
      :class="{ 'content-scroll': scrollable }"
      ref="contentRef"
      @scroll="handleScroll"
    >
      <slot></slot>
    </div>
    
    <!-- 底部标签栏 -->
    <TabBar v-if="showTabbar" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from './NavBar.vue'
import TabBar from './TabBar.vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  showNavbar: {
    type: Boolean,
    default: true
  },
  showBack: {
    type: Boolean,
    default: false
  },
  showTabbar: {
    type: Boolean,
    default: true
  },
  scrollable: {
    type: Boolean,
    default: true
  },
  navTransparent: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['scroll', 'back'])

const router = useRouter()
const contentRef = ref(null)

const handleBack = () => {
  emit('back')
  router.back()
}

const handleScroll = (e) => {
  emit('scroll', {
    scrollTop: e.target.scrollTop,
    scrollHeight: e.target.scrollHeight,
    clientHeight: e.target.clientHeight
  })
}

// 暴露方法给父组件
defineExpose({
  scrollTo: (options) => {
    contentRef.value?.scrollTo(options)
  },
  scrollToTop: () => {
    contentRef.value?.scrollTo({ top: 0, behavior: 'smooth' })
  }
})
</script>

<style lang="scss" scoped>
.page-layout {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
  
  &.has-navbar:not(.nav-transparent) .page-content {
    padding-top: $navbar-height;
  }
  
  &.has-tabbar .page-content {
    padding-bottom: $tabbar-height;
  }
}

.page-content {
  flex: 1;
  position: relative;
  
  &.content-scroll {
    overflow-y: auto;
    overflow-x: hidden;
    -webkit-overflow-scrolling: touch;
    
    // 柔和的滚动条
    &::-webkit-scrollbar {
      width: 3px;
    }
    
    &::-webkit-scrollbar-thumb {
      background: rgba($lavender, 0.3);
      border-radius: 3px;
    }
  }
}
</style>
