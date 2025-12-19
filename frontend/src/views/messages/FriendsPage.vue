<template>
  <PageLayout title="通讯录" :show-back="true" :show-tabbar="false">
    <div class="friends-page">
      <!-- 快速操作栏 -->
      <div class="quick-actions">
        <van-grid :column-num="3" :gutter="12">
          <van-grid-item
            icon="plus"
            text="添加好友"
            @click="goToAddFriend"
          />
          <van-grid-item
            icon="friends-o"
            text="好友申请"
            @click="goToFriendRequests"
            :badge="pendingCount > 0 ? pendingCount : null"
          />
          <van-grid-item
            icon="search"
            text="搜索用户"
            @click="goToSearch"
          />
        </van-grid>
      </div>

      <div class="divider"></div>

      <!-- 搜索框 -->
      <div class="search-section" v-if="showSearch">
        <van-search
          v-model="searchKeyword"
          placeholder="搜索好友昵称或用户名"
          @search="handleSearch"
          @clear="handleClear"
          show-action
          shape="round"
          background="transparent"
        >
          <template #action>
            <div @click="handleCancelSearch">取消</div>
          </template>
        </van-search>
      </div>

      <div v-if="loading" class="loading-container">
        <Loading text="加载中..." />
      </div>

      <template v-else>
        <div v-if="filteredFriends.length > 0" class="friend-list">
          <div
            v-for="friend in filteredFriends"
            :key="friend.id"
            class="friend-item"
            @click="goToProfile(friend.id)"
          >
            <img :src="friend.avatar || '/default-avatar.png'" class="avatar" />
            <div class="friend-info">
              <span class="friend-name">{{ friend.nickname }}</span>
              <span class="friend-username">@{{ friend.username }}</span>
            </div>
<<<<<<< HEAD
            <div class="friend-actions">
              <button
                class="btn btn--ghost btn--small"
                @click.stop="showDeleteConfirm(friend)"
              >
                删除
              </button>
            </div>
=======
            <van-icon name="arrow" class="arrow-icon" />
>>>>>>> d8744d57c20d13d05bc3f5f23b8afb107f11d2e8
          </div>
        </div>

        <div v-else class="empty-state">
<<<<<<< HEAD
          <span class="empty-state__icon">{{ showSearch ? '🔍' : '👋' }}</span>
          <h3 class="empty-state__title">{{ showSearch ? '未找到匹配的好友' : '暂无好友' }}</h3>
          <p class="empty-state__desc">{{ showSearch ? '尝试使用其他关键词搜索' : '点击上方的"添加好友"开始社交吧' }}</p>
=======
          <van-icon name="friends-o" class="empty-state__icon" />
          <h3 class="empty-state__title">暂无好友</h3>
          <p class="empty-state__desc">快去添加好友开始社交吧</p>
>>>>>>> d8744d57c20d13d05bc3f5f23b8afb107f11d2e8
        </div>
      </template>
    </div>
  </PageLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { showDialog, showToast } from 'vant'
import PageLayout from '@/components/layout/PageLayout.vue'
import Loading from '@/components/common/Loading.vue'
import { friendsApi } from '@/api/friends'

const router = useRouter()

const friends = ref([])
const loading = ref(true)
const pendingCount = ref(0)
const showSearch = ref(false)
const searchKeyword = ref('')

// 过滤后的好友列表
const filteredFriends = computed(() => {
  if (!showSearch.value || !searchKeyword.value.trim()) {
    return friends.value
  }

  const keyword = searchKeyword.value.toLowerCase()
  return friends.value.filter(friend =>
    friend.nickname.toLowerCase().includes(keyword) ||
    friend.username.toLowerCase().includes(keyword)
  )
})

const fetchFriends = async () => {
  try {
    const response = await friendsApi.getFriendList()
    friends.value = response.results || response
  } catch (error) {
    console.error('Fetch friends error:', error)
  } finally {
    loading.value = false
  }
}

const fetchPendingCount = async () => {
  try {
    const response = await friendsApi.getPendingRequests()
    pendingCount.value = response.results ? response.results.length : response.length
  } catch (error) {
    console.error('Fetch pending count error:', error)
  }
}

const goToProfile = (id) => {
  router.push(`/user/${id}`)
}

const goToAddFriend = () => {
  router.push('/add-friend')
}

const goToFriendRequests = () => {
  router.push('/friend-requests')
}

const goToSearch = () => {
  showSearch.value = true
}

const handleSearch = () => {
  // 搜索逻辑已在computed中实现
}

const handleClear = () => {
  searchKeyword.value = ''
}

const handleCancelSearch = () => {
  showSearch.value = false
  searchKeyword.value = ''
}

const showDeleteConfirm = (friend) => {
  showDialog({
    title: '删除好友',
    message: `确定要删除好友 "${friend.nickname}" 吗？删除后将无法看到对方的动态。`,
    confirmButtonText: '确定删除',
    confirmButtonColor: '#ff4757',
    showCancelButton: true
  }).then(async () => {
    try {
      await friendsApi.deleteFriend(friend.id)
      friends.value = friends.value.filter(f => f.id !== friend.id)
      showToast({
        message: '好友已删除',
        type: 'success'
      })
    } catch (error) {
      console.error('Delete friend error:', error)
      showToast({
        message: error.response?.data?.detail || '删除失败',
        type: 'fail'
      })
    }
  }).catch(() => {
    // 用户取消操作
  })
}

onMounted(() => {
  fetchFriends()
  fetchPendingCount()
})
</script>

<style lang="scss" scoped>
.friends-page {
  height: 100%;
  padding: $spacing-md;
  display: flex;
  flex-direction: column;
}

.quick-actions {
  margin-bottom: $spacing-md;
}

.divider {
  height: 1px;
  background: $glass-border-light;
  margin: $spacing-md 0;
}

.search-section {
  margin-bottom: $spacing-md;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: $spacing-xl;
}

.friend-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
  flex: 1;
}

.friend-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-md;
  background: $glass-bg;
  backdrop-filter: $glass-blur;
  border: $glass-border-light;
  border-radius: $radius-lg;
  cursor: pointer;
  transition: all $transition-fast;
  box-shadow: $shadow-sm;

  &:hover {
    background: $glass-bg-heavy;
    transform: translateX(4px);
  }
}

.friend-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.friend-name {
  font-size: $font-size-base;
  font-weight: $font-weight-medium;
  color: $text-primary;
}

.friend-username {
  font-size: $font-size-sm;
  color: $text-muted;
}

.friend-actions {
  display: flex;
  gap: $spacing-xs;
}

.arrow-icon {
  font-size: 20px;
  color: $text-muted;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: $spacing-xl;
  flex: 1;
}

.empty-state__icon {
  font-size: 48px;
  margin-bottom: $spacing-md;
  opacity: 0.6;
}

.empty-state__title {
  font-size: $font-size-lg;
  font-weight: $font-weight-medium;
  color: $text-primary;
  margin-bottom: $spacing-sm;
}

.empty-state__desc {
  font-size: $font-size-sm;
  color: $text-muted;
  line-height: 1.5;
}
</style>

