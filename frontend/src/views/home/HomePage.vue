<template>
  <PageLayout title="朋友圈" :show-back="false">
    <template #nav-right>
      <button class="nav-btn" @click="refreshFeed">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M23 4v6h-6M1 20v-6h6"/>
          <path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/>
        </svg>
      </button>
    </template>
    
    <div class="home-page">
      <PullRefresh @refresh="onRefresh">
        <!-- 动态列表 -->
        <div class="feed-list">
          <MomentCard 
            v-for="moment in moments" 
            :key="moment.id"
            :moment="moment"
            @click="goToDetail(moment.id)"
          />
          
          <!-- 加载更多 -->
          <div v-if="loading" class="loading-more">
            <Loading text="加载中..." />
          </div>
          
          <!-- 空状态 -->
          <div v-else-if="moments.length === 0" class="empty-container">
            <div class="empty-state">
              <span class="empty-state__icon">📭</span>
              <h3 class="empty-state__title">暂无动态</h3>
              <p class="empty-state__desc">快去添加好友，查看他们的精彩分享吧</p>
            </div>
          </div>
          
          <!-- 加载完成 -->
          <div v-else-if="!hasMore" class="load-complete">
            <span class="load-complete__line"></span>
            <span class="load-complete__text">没有更多了</span>
            <span class="load-complete__line"></span>
          </div>
        </div>
      </PullRefresh>
    </div>
  </PageLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PageLayout from '@/components/layout/PageLayout.vue'
import PullRefresh from '@/components/common/PullRefresh.vue'
import Loading from '@/components/common/Loading.vue'
import MomentCard from '@/components/business/MomentCard.vue'
import { momentsApi } from '@/api/moments'

const router = useRouter()

const moments = ref([])
const loading = ref(false)
const page = ref(1)
const hasMore = ref(true)

const fetchFeed = async (isRefresh = false) => {
  if (loading.value) return
  
  loading.value = true
  
  try {
    if (isRefresh) {
      page.value = 1
      moments.value = []
    }
    
    const response = await momentsApi.getFeed(page.value)
    
    if (isRefresh) {
      moments.value = response.results
    } else {
      moments.value.push(...response.results)
    }
    
    hasMore.value = !!response.next
    page.value++
  } catch (error) {
    console.error('Fetch feed error:', error)
  } finally {
    loading.value = false
  }
}

const onRefresh = (done) => {
  fetchFeed(true).finally(() => {
    done()
  })
}

const refreshFeed = () => {
  fetchFeed(true)
}

const goToDetail = (id) => {
  router.push(`/moment/${id}`)
}

onMounted(() => {
  fetchFeed()
})
</script>

<style lang="scss" scoped>
.home-page {
  height: 100%;
}

.nav-btn {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: $glass-bg;
  backdrop-filter: $glass-blur;
  -webkit-backdrop-filter: $glass-blur;
  border: $glass-border-light;
  border-radius: 50%;
  transition: all $transition-normal;
  box-shadow: 0 4px 12px rgba(183, 168, 214, 0.2);
  
  svg {
    width: 18px;
    height: 18px;
    color: $text-primary;
  }
  
  &:hover {
    background: rgba(255, 255, 255, 0.7);
    transform: rotate(180deg);
    box-shadow: 0 6px 16px rgba(183, 168, 214, 0.3);
  }
  
  &:active {
    transform: scale(0.95);
  }
}

.feed-list {
  padding: $spacing-md;
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.loading-more {
  padding: $spacing-lg;
}

.empty-container {
  padding: $spacing-2xl $spacing-md;
}

.load-complete {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: $spacing-md;
  padding: $spacing-xl $spacing-lg;
  
  &__line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba($lavender, 0.3), transparent);
  }
  
  &__text {
    font-size: $font-size-sm;
    color: $text-muted;
    white-space: nowrap;
  }
}
</style>
