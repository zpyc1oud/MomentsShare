<template>
  <PageLayout title="发现" :show-back="false">
    <div class="discover-page">
      <!-- 搜索栏 -->
      <div class="search-bar">
        <div class="search-input-wrapper">
          <van-icon name="search" class="search-icon" />
          <input 
            ref="searchInputRef"
            v-model="searchForm.keyword"
            type="search"
            class="search-input"
            placeholder="搜索动态内容..."
            @keyup.enter="handleSearch"
            @input="handleInputChange"
            @focus="handleInputFocus"
            @blur="handleInputBlur"
          />
          <!-- 一键清除按钮 -->
          <transition name="fade">
            <button 
              v-if="searchForm.keyword" 
              class="clear-btn"
              @mousedown.prevent="clearInput"
            >
              <van-icon name="cross" />
            </button>
          </transition>
          
          <!-- 搜索建议/历史/热门下拉列表 -->
          <transition name="fade">
            <div 
              v-if="showDropdown" 
              class="suggestions-dropdown"
              @mousedown.prevent
            >
              <!-- 搜索建议 -->
              <template v-if="searchForm.keyword && (suggestions.length > 0 || tagSuggestions.length > 0)">
                <div 
                  v-for="(item, index) in suggestions" 
                  :key="'suggestion-' + index"
                  class="suggestion-item suggestion-item--moment"
                  @mousedown.prevent="selectSuggestion(item)"
                >
                  <van-icon name="search" class="suggestion-icon" />
                  <div class="suggestion-content">
                    <span class="suggestion-text" v-html="highlightKeyword(item.text, item.keyword)"></span>
                    <span class="suggestion-type suggestion-type--moment">动态</span>
                  </div>
                </div>
                <div 
                  v-for="tag in tagSuggestions" 
                  :key="'tag-' + tag.id"
                  class="suggestion-item suggestion-item--tag"
                  @mousedown.prevent="selectTag(tag.name)"
                >
                  <van-icon name="label-o" class="suggestion-icon" />
                  <div class="suggestion-content">
                    <span class="suggestion-text" v-html="highlightKeyword(tag.name, searchForm.keyword)"></span>
                    <span class="suggestion-type suggestion-type--tag">标签</span>
                  </div>
                </div>
              </template>
              
              <!-- 搜索历史和热门搜索（未输入时显示） -->
              <template v-else>
                <!-- 搜索历史 -->
                <div v-if="searchHistory.length > 0" class="dropdown-section">
                  <div class="section-header">
                    <span class="section-title">搜索历史</span>
                    <button class="clear-history-btn" @click="clearAllHistory">
                      <van-icon name="delete-o" />
                    </button>
                  </div>
                  <div 
                    v-for="(keyword, index) in searchHistory" 
                    :key="'history-' + index"
                    class="suggestion-item suggestion-item--history"
                    @mousedown.prevent="selectHistory(keyword)"
                  >
                    <van-icon name="clock-o" class="suggestion-icon" />
                    <div class="suggestion-content">
                      <span class="suggestion-text">{{ keyword }}</span>
                    </div>
                    <button 
                      class="delete-history-btn"
                      @mousedown.stop.prevent="removeHistory(keyword)"
                    >
                      <van-icon name="cross" />
                    </button>
                  </div>
                </div>
                
                <!-- 热门搜索 -->
                <div v-if="hotTags.length > 0" class="dropdown-section">
                  <div class="section-header">
                    <span class="section-title">热门搜索</span>
                  </div>
                  <div class="hot-tags">
                    <span 
                      v-for="tag in hotTags" 
                      :key="'hot-' + tag.id"
                      class="hot-tag"
                      @mousedown.prevent="selectTag(tag.name)"
                    >
                      <van-icon name="fire" class="hot-tag-icon" />
                      {{ tag.name }}
                    </span>
                  </div>
                </div>
              </template>
            </div>
          </transition>
          
          <!-- 遮罩层 -->
          <transition name="fade">
            <div 
              v-if="showDropdown" 
              class="dropdown-overlay"
              @mousedown.prevent="closeDropdown"
            ></div>
          </transition>
        </div>
        <button class="filter-btn" @click="showFilter = !showFilter">
          <van-icon name="filter-o" />
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
            <van-icon name="search" class="empty-state__icon" />
            <h3 class="empty-state__title">未找到结果</h3>
            <p class="empty-state__desc">尝试更换关键词或筛选条件</p>
            <!-- 空状态推荐 -->
            <div v-if="hotTags.length > 0" class="empty-state-recommend">
              <p class="recommend-title">试试这些热门标签：</p>
              <div class="recommend-tags">
                <span 
                  v-for="tag in hotTags.slice(0, 5)" 
                  :key="'recommend-' + tag.id"
                  class="recommend-tag"
                  @click="selectTag(tag.name)"
                >
                  {{ tag.name }}
                </span>
              </div>
            </div>
          </div>
        </template>
        
        <div v-else class="discover-hint">
          <van-icon name="bulb-o" class="hint-icon" />
          <p>输入关键词搜索动态，或使用筛选器精确查找</p>
        </div>
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import PageLayout from '@/components/layout/PageLayout.vue'
import Loading from '@/components/common/Loading.vue'
import MomentCard from '@/components/business/MomentCard.vue'
import { momentsApi } from '@/api/moments'
import { 
  getSearchHistory, 
  saveSearchHistory, 
  removeSearchHistory, 
  clearSearchHistory 
} from '@/utils/searchHistory'

const router = useRouter()
const searchInputRef = ref(null)

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
const suggestions = ref([])
const tagSuggestions = ref([])
const hotTags = ref([])
const searchHistory = ref([])
const showSuggestions = ref(false)
const isInputFocused = ref(false)
let suggestionTimer = null

// 计算是否显示下拉列表
const showDropdown = computed(() => {
  if (!isInputFocused.value) return false
  
  // 有输入时显示建议
  if (searchForm.keyword && (suggestions.value.length > 0 || tagSuggestions.value.length > 0)) {
    return true
  }
  
  // 无输入时显示历史和热门
  if (!searchForm.keyword && (searchHistory.value.length > 0 || hotTags.value.length > 0)) {
    return true
  }
  
  return false
})

// 加载搜索历史和热门搜索
onMounted(async () => {
  searchHistory.value = getSearchHistory()
  await loadHotTags()
})

// 加载热门标签
const loadHotTags = async () => {
  try {
    const response = await momentsApi.getHotSearch()
    hotTags.value = response.tags || []
  } catch (error) {
    console.error('Load hot tags error:', error)
  }
}

// 防抖获取搜索建议
const fetchSuggestions = async (keyword) => {
  if (!keyword || keyword.trim().length < 1) {
    suggestions.value = []
    tagSuggestions.value = []
    return
  }

  try {
    const trimmedKeyword = keyword.trim()
    console.log('🔍 获取搜索建议，关键词:', trimmedKeyword)
    const response = await momentsApi.getSuggestions(trimmedKeyword, 8)
    console.log('📥 搜索建议响应:', response)
    suggestions.value = response.suggestions || []
    tagSuggestions.value = response.tags || []
    console.log('✅ 建议数量:', suggestions.value.length, '标签数量:', tagSuggestions.value.length)
  } catch (error) {
    console.error('❌ 获取搜索建议失败:', error)
    console.error('错误详情:', error.response?.data || error.message)
    suggestions.value = []
    tagSuggestions.value = []
  }
}

const handleInputChange = () => {
  // 清除之前的定时器
  if (suggestionTimer) {
    clearTimeout(suggestionTimer)
  }
  
  // 防抖：300ms后获取建议
  suggestionTimer = setTimeout(() => {
    fetchSuggestions(searchForm.keyword)
  }, 300)
}

const handleInputFocus = () => {
  isInputFocused.value = true
  // 如果已有输入，刷新建议
  if (searchForm.keyword) {
    fetchSuggestions(searchForm.keyword)
  }
}

const handleInputBlur = () => {
  // 延迟隐藏，以便点击建议项时能触发
  setTimeout(() => {
    isInputFocused.value = false
  }, 200)
}

const closeDropdown = () => {
  isInputFocused.value = false
  if (searchInputRef.value) {
    searchInputRef.value.blur()
  }
}

const clearInput = () => {
  searchForm.keyword = ''
  suggestions.value = []
  tagSuggestions.value = []
  if (searchInputRef.value) {
    searchInputRef.value.focus()
  }
}

const selectSuggestion = (item) => {
  const keyword = item.keyword || item.text.trim()
  searchForm.keyword = keyword
  saveSearchHistory(keyword)
  searchHistory.value = getSearchHistory()
  closeDropdown()
  
  if (item.moment_id) {
    goToDetail(item.moment_id)
  } else {
    handleSearch()
  }
}

const selectTag = (tagName) => {
  searchForm.keyword = tagName
  searchForm.label = tagName
  saveSearchHistory(tagName)
  searchHistory.value = getSearchHistory()
  closeDropdown()
  handleSearch()
}

const selectHistory = (keyword) => {
  searchForm.keyword = keyword
  closeDropdown()
  handleSearch()
}

const removeHistory = (keyword) => {
  removeSearchHistory(keyword)
  searchHistory.value = getSearchHistory()
}

const clearAllHistory = () => {
  clearSearchHistory()
  searchHistory.value = []
}

// 高亮关键词
const highlightKeyword = (text, keyword) => {
  if (!keyword || !text) return text
  const regex = new RegExp(`(${keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

const handleSearch = async () => {
  if (!searchForm.keyword && !searchForm.label && !searchForm.start_date) {
    return
  }
  
  // 保存搜索历史
  if (searchForm.keyword) {
    saveSearchHistory(searchForm.keyword)
    searchHistory.value = getSearchHistory()
  }
  
  closeDropdown()
  loading.value = true
  hasSearched.value = true
  
  try {
    const params = {}
    if (searchForm.keyword) params.keyword = searchForm.keyword
    if (searchForm.label) params.label = searchForm.label
    if (searchForm.start_date) params.start_date = searchForm.start_date
    if (searchForm.end_date) params.end_date = searchForm.end_date
    
    console.log('🔍 执行搜索，参数:', params)
    const response = await momentsApi.search(params)
    console.log('📥 搜索结果响应:', response)
    console.log('📊 结果数量:', response.results?.length || 0)
    
    // 结果去重
    const seenIds = new Set()
    results.value = (response.results || []).filter(moment => {
      if (seenIds.has(moment.id)) {
        return false
      }
      seenIds.add(moment.id)
      return true
    })
    console.log('✅ 去重后结果数量:', results.value.length)
  } catch (error) {
    console.error('❌ 搜索失败:', error)
    console.error('错误详情:', error.response?.data || error.message)
    results.value = []
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
  suggestions.value = []
  tagSuggestions.value = []
  closeDropdown()
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
  background: transparent;
  position: relative;
  z-index: 10;
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
    z-index: 2;
    pointer-events: none;
  }
  
  .search-input {
    width: 100%;
    padding: 12px 44px 12px 44px;
    background: $glass-bg-heavy;
    backdrop-filter: $glass-blur;
    border: $glass-border;
    border-radius: $radius-full;
    color: $text-primary;
    font-size: $font-size-base;
    
    &:focus {
      border-color: rgba($pink-primary, 0.5);
      outline: none;
    }
    
    // 移动端键盘显示搜索图标
    &[type="search"] {
      -webkit-appearance: none;
    }
  }

  .clear-btn {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2);
    border: none;
    border-radius: 50%;
    color: $text-muted;
    cursor: pointer;
    z-index: 2;
    transition: all 0.2s;
    
    &:hover {
      background: rgba(255, 255, 255, 0.3);
      color: $text-primary;
    }
    
    svg {
      width: 14px;
      height: 14px;
    }
  }

  .dropdown-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(2px);
    z-index: 999;
  }

  .suggestions-dropdown {
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    right: 0;
    background: $glass-bg-heavy;
    backdrop-filter: $glass-blur;
    border: $glass-border;
    border-radius: $radius-md;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    max-height: 400px;
    overflow-y: auto;
    z-index: 1000;
    margin-top: 4px;
  }

  .dropdown-section {
    padding: 8px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    
    &:last-child {
      border-bottom: none;
    }
  }

  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 16px;
    margin-bottom: 4px;
  }

  .section-title {
    font-size: $font-size-xs;
    color: $text-muted;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .clear-history-btn {
    background: none;
    border: none;
    color: $text-muted;
    cursor: pointer;
    padding: 4px;
    display: flex;
    align-items: center;
    
    &:hover {
      color: $text-primary;
    }
    
    svg {
      width: 14px;
      height: 14px;
    }
  }

  .suggestion-item {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    cursor: pointer;
    transition: background-color 0.2s;
    position: relative;

    &:hover {
      background: rgba(255, 255, 255, 0.1);
    }

    &--moment {
      .suggestion-icon {
        color: rgba($pink-primary, 0.8);
      }
    }

    &--tag {
      .suggestion-icon {
        color: rgba(66, 165, 245, 0.8);
      }
    }

    &--history {
      .suggestion-icon {
        color: $text-muted;
      }
    }

    .suggestion-icon {
      width: 18px;
      height: 18px;
      margin-right: 12px;
      flex-shrink: 0;
    }

    .suggestion-content {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      min-width: 0;
    }

    .suggestion-text {
      flex: 1;
      font-size: $font-size-sm;
      color: $text-primary;
      line-height: 1.4;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;

      :deep(mark) {
        background: rgba($pink-primary, 0.3);
        color: $pink-primary;
        font-weight: 500;
        padding: 0 2px;
        border-radius: 2px;
      }
    }

    .suggestion-type {
      font-size: $font-size-xs;
      padding: 2px 8px;
      border-radius: $radius-sm;
      flex-shrink: 0;
      font-weight: 500;
      
      &--moment {
        background: rgba($pink-primary, 0.2);
        color: $pink-primary;
      }
      
      &--tag {
        background: rgba(66, 165, 245, 0.2);
        color: #42a5f5;
      }
    }

    .delete-history-btn {
      background: none;
      border: none;
      color: $text-muted;
      cursor: pointer;
      padding: 4px;
      display: flex;
      align-items: center;
      opacity: 0;
      transition: opacity 0.2s;
      
      &:hover {
        color: $text-primary;
      }
      
      svg {
        width: 14px;
        height: 14px;
      }
    }

    &:hover .delete-history-btn {
      opacity: 1;
    }
  }

  .hot-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 8px 16px;
  }

  .hot-tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 6px 12px;
    background: rgba($pink-primary, 0.15);
    border: 1px solid rgba($pink-primary, 0.3);
    border-radius: $radius-full;
    color: $pink-primary;
    font-size: $font-size-sm;
    cursor: pointer;
    transition: all 0.2s;
    
    &:hover {
      background: rgba($pink-primary, 0.25);
      border-color: rgba($pink-primary, 0.5);
      transform: translateY(-1px);
    }
    
    .hot-tag-icon {
      width: 14px;
      height: 14px;
      color: #ff6b6b;
    }
  }
}

.filter-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: $glass-bg-heavy;
  backdrop-filter: $glass-blur;
  border: $glass-border;
  border-radius: $radius-md;
  color: $text-secondary;
  cursor: pointer;
  
  svg {
    width: 20px;
    height: 20px;
  }
}

.filter-panel {
  padding: $spacing-md;
  background: $glass-bg;
  backdrop-filter: $glass-blur;
  border-bottom: $glass-border-light;
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
  background: $glass-bg-heavy;
  border: $glass-border;
  border-radius: $radius-sm;
  color: $text-primary;
  font-size: $font-size-sm;
  
  &:focus {
    border-color: rgba($pink-primary, 0.5);
    outline: none;
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
    color: $text-muted;
  }
  
  p {
    font-size: $font-size-sm;
    color: $text-muted;
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-xl;
  text-align: center;
  
  &__icon {
    font-size: 64px;
    margin-bottom: $spacing-md;
    color: $text-muted;
    opacity: 0.5;
  }
  
  &__title {
    font-size: $font-size-lg;
    color: $text-primary;
    margin-bottom: $spacing-sm;
  }
  
  &__desc {
    font-size: $font-size-sm;
    color: $text-muted;
    margin-bottom: $spacing-lg;
  }
}

.empty-state-recommend {
  margin-top: $spacing-lg;
  padding-top: $spacing-lg;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  
  .recommend-title {
    font-size: $font-size-sm;
    color: $text-secondary;
    margin-bottom: $spacing-md;
  }
  
  .recommend-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
  }
  
  .recommend-tag {
    padding: 6px 14px;
    background: rgba($pink-primary, 0.15);
    border: 1px solid rgba($pink-primary, 0.3);
    border-radius: $radius-full;
    color: $pink-primary;
    font-size: $font-size-sm;
    cursor: pointer;
    transition: all 0.2s;
    
    &:hover {
      background: rgba($pink-primary, 0.25);
      border-color: rgba($pink-primary, 0.5);
      transform: translateY(-1px);
    }
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}
</style>
