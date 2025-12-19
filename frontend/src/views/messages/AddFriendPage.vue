<template>
  <PageLayout title="添加好友" :show-back="true" :show-tabbar="false">
    <div class="add-friend-page">
      <!-- 搜索框 -->
      <div class="search-section">
        <van-search
          v-model="searchKeyword"
          placeholder="搜索昵称或手机号"
          @search="handleSearch"
          @clear="handleClear"
          show-action
          shape="round"
          background="transparent"
        >
          <template #action>
            <div @click="handleSearch">搜索</div>
          </template>
        </van-search>
      </div>

      <!-- 搜索结果 -->
      <div v-if="loading" class="loading-container">
        <Loading text="搜索中..." />
      </div>

      <template v-else-if="searchKeyword">
        <div v-if="searchResults.length > 0" class="search-results">
          <div
            v-for="user in searchResults"
            :key="user.id"
            class="user-item"
          >
            <img :src="user.avatar || '/default-avatar.png'" class="avatar" />
            <div class="user-info">
              <span class="user-name">{{ user.nickname }}</span>
              <span class="user-phone">{{ user.phone }}</span>
            </div>
            <div class="user-actions">
              <!-- 已添加好友 -->
              <button
                v-if="user.friendship_status === 'ACCEPTED'"
                class="btn btn--ghost btn--small"
                disabled
              >
                已添加
              </button>
              <!-- 已发送申请 -->
              <button
                v-else-if="user.friendship_status === 'PENDING'"
                class="btn btn--ghost btn--small"
                disabled
              >
                已发送
              </button>
              <!-- 被拒绝过，可以重新申请 -->
              <button
                v-else-if="user.friendship_status === 'REJECTED'"
                class="btn btn--primary btn--small"
                @click="handleAddFriend(user)"
                :disabled="addingFriend === user.id"
              >
                {{ addingFriend === user.id ? '发送中...' : '添加' }}
              </button>
              <!-- 无关系，可以添加 -->
              <button
                v-else
                class="btn btn--primary btn--small"
                @click="handleAddFriend(user)"
                :disabled="addingFriend === user.id"
              >
                {{ addingFriend === user.id ? '发送中...' : '添加' }}
              </button>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <span class="empty-state__icon">🔍</span>
          <h3 class="empty-state__title">未找到用户</h3>
          <p class="empty-state__desc">尝试使用其他关键词搜索</p>
        </div>
      </template>

      <!-- 默认状态 -->
      <div v-else class="default-state">
        <span class="default-state__icon">👥</span>
        <h3 class="default-state__title">添加好友</h3>
        <p class="default-state__desc">搜索昵称或手机号来添加新好友</p>
      </div>
    </div>
  </PageLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { showToast } from 'vant'
import PageLayout from '@/components/layout/PageLayout.vue'
import Loading from '@/components/common/Loading.vue'
import { friendsApi } from '@/api/friends'

const searchKeyword = ref('')
const searchResults = ref([])
const loading = ref(false)
const addingFriend = ref(null)

const handleSearch = async () => {
  const keyword = searchKeyword.value.trim()
  if (!keyword) {
    showToast('请输入搜索关键词')
    return
  }

  loading.value = true
  try {
    const response = await friendsApi.searchUsers(keyword)
    searchResults.value = response.results || response
  } catch (error) {
    console.error('Search error:', error)
    showToast({
      message: error.response?.data?.detail || '搜索失败',
      type: 'fail'
    })
  } finally {
    loading.value = false
  }
}

const handleClear = () => {
  searchResults.value = []
  searchKeyword.value = ''
}

const handleAddFriend = async (user) => {
  addingFriend.value = user.id

  try {
    await friendsApi.sendRequest(user.id)
    showToast({
      message: '好友申请已发送',
      type: 'success'
    })

    // 更新用户状态为PENDING，而不是移除
    const userIndex = searchResults.value.findIndex(u => u.id === user.id)
    if (userIndex !== -1) {
      searchResults.value[userIndex].friendship_status = 'PENDING'
    }
  } catch (error) {
    console.error('Add friend error:', error)
    showToast({
      message: error.response?.data?.detail || '发送失败',
      type: 'fail'
    })
  } finally {
    addingFriend.value = null
  }
}

onMounted(() => {
  // 可以在这里添加一些默认行为，比如热门用户推荐
})
</script>

<style lang="scss" scoped>
.add-friend-page {
  height: 100%;
  padding: $spacing-md;
  display: flex;
  flex-direction: column;
}

.search-section {
  margin-bottom: $spacing-md;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: $spacing-xl;
}

.search-results {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.user-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-md;
  background: $glass-bg;
  backdrop-filter: blur(10px);
  border: $glass-border-light;
  border-radius: $radius-lg;
  box-shadow: $shadow-sm;
}

.user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: $font-size-base;
  font-weight: $font-weight-medium;
  color: $text-primary;
}

.user-phone {
  font-size: $font-size-sm;
  color: $text-muted;
  margin-top: 2px;
}

.empty-state,
.default-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: $spacing-xl;
  flex: 1;
}

.empty-state__icon,
.default-state__icon {
  font-size: 48px;
  margin-bottom: $spacing-md;
  opacity: 0.6;
}

.empty-state__title,
.default-state__title {
  font-size: $font-size-lg;
  font-weight: $font-weight-medium;
  color: $text-primary;
  margin-bottom: $spacing-sm;
}

.empty-state__desc,
.default-state__desc {
  font-size: $font-size-sm;
  color: $text-muted;
  line-height: 1.5;
}
</style>