// 搜索历史管理工具
const SEARCH_HISTORY_KEY = 'moments_search_history'
const MAX_HISTORY_COUNT = 10

/**
 * 获取搜索历史
 */
export function getSearchHistory() {
  try {
    const history = localStorage.getItem(SEARCH_HISTORY_KEY)
    return history ? JSON.parse(history) : []
  } catch (error) {
    console.error('Failed to get search history:', error)
    return []
  }
}

/**
 * 保存搜索关键词到历史记录
 */
export function saveSearchHistory(keyword) {
  if (!keyword || !keyword.trim()) {
    return
  }

  try {
    let history = getSearchHistory()
    const trimmedKeyword = keyword.trim()
    
    // 移除重复项
    history = history.filter(item => item !== trimmedKeyword)
    
    // 添加到开头
    history.unshift(trimmedKeyword)
    
    // 限制数量
    if (history.length > MAX_HISTORY_COUNT) {
      history = history.slice(0, MAX_HISTORY_COUNT)
    }
    
    localStorage.setItem(SEARCH_HISTORY_KEY, JSON.stringify(history))
  } catch (error) {
    console.error('Failed to save search history:', error)
  }
}

/**
 * 删除单个历史记录
 */
export function removeSearchHistory(keyword) {
  try {
    let history = getSearchHistory()
    history = history.filter(item => item !== keyword)
    localStorage.setItem(SEARCH_HISTORY_KEY, JSON.stringify(history))
  } catch (error) {
    console.error('Failed to remove search history:', error)
  }
}

/**
 * 清空搜索历史
 */
export function clearSearchHistory() {
  try {
    localStorage.removeItem(SEARCH_HISTORY_KEY)
  } catch (error) {
    console.error('Failed to clear search history:', error)
  }
}

