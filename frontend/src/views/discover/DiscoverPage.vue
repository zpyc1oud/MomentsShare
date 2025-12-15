<template>
  <PageLayout title="发现" :show-back="false">
    <div class="discover-page">
      <!-- 搜索栏 -->
      <div class="search-bar">
        <div class="search-input-wrapper">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
          </svg>
          <input 
            v-model="searchForm.keyword"
            type="text"
            class="search-input"
            placeholder="搜索动态内容..."
            @keyup.enter="handleSearch"
          />
        </div>
        <button class="filter-btn" @click="showFilter = !showFilter">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>
          </svg>
        </button>
      </div>
      
      <!-- 筛选面板 -->
      <transition name="slide">
        <div v-if="showFilter" class="filter-panel">
          <div class="filter-group">
            <label class="filter-label">标签</label>
            <input 
              v-model="searchForm.label"
              type="text"
              class="filter-input"
              placeholder="输入标签名称"
            />
          </div>
          <div class="filter-group">
            <label class="filter-label">开始日期</label>
            <input 
              v-model="searchForm.start_date"
              type="date"
              class="filter-input"
            />
          </div>
          <div class="filter-group">
            <label class="filter-label">结束日期</label>
            <input 
              v-model="searchForm.end_date"
              type="date"
              class="filter-input"
            />
          </div>
          <div class="filter-actions">
            <button class="btn btn--secondary btn--small" @click="resetFilter">重置</button>
            <button class="btn btn--primary btn--small" @click="handleSearch">搜索</button>
          </div>
        </div>
      </transition>
      
      <!-- 搜索结果 -->
      <div class="search-results">
        <div v-if="loading" class="loading-container">
          <Loading text="搜索中..." />
        </div>
        
        <template v-else-if="hasSearched">
          <div v-if="results.length > 0" class="results-list">
            <MomentCard 
              v-for="moment in results" 
              :key="moment.id"
              :moment="moment"
              @click="goToDetail(moment.id)"
            />
          </div>
          
          <div v-else class="empty-state">
            <span class="empty-state__icon">🔍</span>
            <h3 class="empty-state__title">未找到结果</h3>
            <p class="empty-state__desc">尝试更换关键词或筛选条件</p>
          </div>
        </template>
        
        <div v-else class="discover-hint">
          <span class="hint-icon">💡</span>
          <p>输入关键词搜索动态，或使用筛选器精确查找</p>
        </div>
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import PageLayout from '@/components/layout/PageLayout.vue'
import Loading from '@/components/common/Loading.vue'
import MomentCard from '@/components/business/MomentCard.vue'
import { momentsApi } from '@/api/moments'

const router = useRouter()

const searchForm = reactive({
  keyword: '',
  label: '',
  start_date: '',
  end_date: ''
})

const showFilter = ref(false)
const loading = ref(false)
const hasSearched = ref(false)
const results = ref([])

const handleSearch = async () => {
  if (!searchForm.keyword && !searchForm.label && !searchForm.start_date) {
    return
  }
  
  loading.value = true
  hasSearched.value = true
  
  try {
    const params = {}
    if (searchForm.keyword) params.keyword = searchForm.keyword
    if (searchForm.label) params.label = searchForm.label
    if (searchForm.start_date) params.start_date = searchForm.start_date
    if (searchForm.end_date) params.end_date = searchForm.end_date
    
    const response = await momentsApi.search(params)
    results.value = response.results
  } catch (error) {
    console.error('Search error:', error)
  } finally {
    loading.value = false
  }
}

const resetFilter = () => {
  searchForm.keyword = ''
  searchForm.label = ''
  searchForm.start_date = ''
  searchForm.end_date = ''
  results.value = []
  hasSearched.value = false
}

const goToDetail = (id) => {
  router.push(`/moment/${id}`)
}
</script>

<style lang="scss" scoped>
.discover-page {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.search-bar {
  display: flex;
  gap: $spacing-sm;
  padding: $spacing-md;
  background: $bg-dark;
}

.search-input-wrapper {
  flex: 1;
  position: relative;
  
  .search-icon {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    width: 18px;
    height: 18px;
    color: $text-muted;
  }
  
  .search-input {
    width: 100%;
    padding: 12px 12px 12px 44px;
    background: $bg-input;
    border: 1px solid $border-color;
    border-radius: $radius-full;
    color: $text-primary;
    font-size: $font-size-base;
    
    &:focus {
      border-color: $primary-color;
    }
  }
}

.filter-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: $bg-input;
  border: 1px solid $border-color;
  border-radius: $radius-md;
  color: $text-secondary;
  
  svg {
    width: 20px;
    height: 20px;
  }
}

.filter-panel {
  padding: $spacing-md;
  background: $bg-card;
  border-bottom: 1px solid $border-light;
}

.filter-group {
  margin-bottom: $spacing-md;
}

.filter-label {
  display: block;
  font-size: $font-size-sm;
  color: $text-secondary;
  margin-bottom: $spacing-xs;
}

.filter-input {
  width: 100%;
  padding: 10px 12px;
  background: $bg-input;
  border: 1px solid $border-color;
  border-radius: $radius-sm;
  color: $text-primary;
  font-size: $font-size-sm;
  
  &:focus {
    border-color: $primary-color;
  }
}

.filter-actions {
  display: flex;
  gap: $spacing-sm;
  justify-content: flex-end;
}

.search-results {
  flex: 1;
  overflow-y: auto;
  padding: $spacing-md;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: $spacing-xl;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.discover-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-xl;
  text-align: center;
  
  .hint-icon {
    font-size: 48px;
    margin-bottom: $spacing-md;
  }
  
  p {
    font-size: $font-size-sm;
    color: $text-muted;
  }
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>

