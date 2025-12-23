<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <el-aside :width="sidebarWidth" class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <img src="/src/assets/icon.png" alt="Logo" class="logo-img" />
          <span v-show="!isCollapse" class="logo-text">MomentsShare</span>
        </div>
      </div>

      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :unique-opened="true"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon>
          <template #title>数据看板</template>
        </el-menu-item>

        <el-sub-menu index="content">
          <template #title>
            <el-icon><Document /></el-icon>
            <span>内容管理</span>
          </template>
          <el-menu-item index="/dashboard/content/moments">
            <el-icon><Picture /></el-icon>
            <template #title>动态管理</template>
          </el-menu-item>
          <el-menu-item index="/dashboard/content/comments">
            <el-icon><ChatDotRound /></el-icon>
            <template #title>评论管理</template>
          </el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="user">
          <template #title>
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </template>
          <el-menu-item index="/dashboard/user/list">
            <el-icon><UserFilled /></el-icon>
            <template #title>用户列表</template>
          </el-menu-item>
          <el-menu-item index="/dashboard/user/growth">
            <el-icon><TrendCharts /></el-icon>
            <template #title>增长分析</template>
          </el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/dashboard/settings">
          <el-icon><Setting /></el-icon>
          <template #title>系统设置</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区域 -->
    <el-container class="main-container">
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="header-left">
          <el-button
            type="text"
            class="collapse-btn"
            @click="toggleSidebar"
          >
            <el-icon :size="20">
              <Expand v-if="isCollapse" />
              <Fold v-else />
            </el-icon>
          </el-button>

          <el-breadcrumb separator="/" class="breadcrumb">
            <el-breadcrumb-item
              v-for="item in breadcrumbList"
              :key="item.path"
              :to="item.path"
            >
              {{ item.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <div class="user-info">
              <el-avatar :size="32" class="user-avatar">
                <el-icon><UserFilled /></el-icon>
              </el-avatar>
              <span class="username">管理员</span>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人信息
                </el-dropdown-item>
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon>
                  系统设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 主要内容 -->
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// 侧边栏折叠状态
const isCollapse = ref(false)
const sidebarWidth = computed(() => isCollapse.value ? '64px' : '200px')

// 当前激活的菜单
const activeMenu = computed(() => {
  const { path } = route
  if (path.startsWith('/dashboard')) return '/dashboard'
  if (path.startsWith('/content/moments')) return '/content/moments'
  if (path.startsWith('/content/comments')) return '/content/comments'
  if (path.startsWith('/user/list')) return '/user/list'
  if (path.startsWith('/user/growth')) return '/user/growth'
  if (path.startsWith('/settings')) return '/settings'
  return path
})

// 面包屑导航
const breadcrumbList = computed(() => {
  const { path, meta } = route
  const breadcrumbs = []

  if (path.startsWith('/dashboard')) {
    breadcrumbs.push({ title: '首页', path: '/dashboard' })
    if (meta.title && meta.title !== '数据看板') {
      breadcrumbs.push({ title: meta.title, path: path })
    }
  } else if (path.startsWith('/content')) {
    breadcrumbs.push({ title: '首页', path: '/dashboard' })
    breadcrumbs.push({ title: '内容管理', path: '/content' })
    if (meta.title && meta.title !== '内容管理') {
      breadcrumbs.push({ title: meta.title, path: path })
    }
  } else if (path.startsWith('/user')) {
    breadcrumbs.push({ title: '首页', path: '/dashboard' })
    breadcrumbs.push({ title: '用户管理', path: '/user' })
    if (meta.title && meta.title !== '用户管理') {
      breadcrumbs.push({ title: meta.title, path: path })
    }
  } else if (path.startsWith('/settings')) {
    breadcrumbs.push({ title: '首页', path: '/dashboard' })
    breadcrumbs.push({ title: '系统设置', path: '/settings' })
  }

  return breadcrumbs
})

// 切换侧边栏
const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

// 处理下拉菜单命令
const handleCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      handleLogout()
      break
  }
}

// 处理退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    await authStore.logout()
    ElMessage.success('退出登录成功')
    router.push('/login')
  } catch (error) {
    // 用户取消操作
  }
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
  display: flex;
  background: var(--mesh-gradient-bg);
  background-attachment: fixed;
}

/* 侧边栏样式 */
.sidebar {
  background: rgba(255, 255, 255, 0.95);
  transition: width 0.3s;
  overflow: hidden;
  backdrop-filter: blur(20px);
  box-shadow: var(--shadow-lg);
  border-right: 1px solid var(--border-color);
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid var(--border-color);
  background: var(--glass-bg-heavy);
}

.logo {
  display: flex;
  align-items: center;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

.logo-img {
  width: 32px;
  height: 32px;
  margin-right: 12px;
  object-fit: contain;
  display: block;
  border-radius: 8px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  white-space: nowrap;
}

.sidebar-menu {
  border: none;
  background: transparent;
  padding: 8px 0;
}

:deep(.el-menu) {
  background: transparent !important;
  border: none !important;
}

:deep(.el-menu-item) {
  color: #9B8DC4 !important;
  background: rgba(255, 255, 255, 0.8) !important;
  border-radius: 12px !important;
  margin: 4px 8px !important;
  transition: all var(--transition-normal) !important;
  font-weight: 600 !important;
  border: 1px solid var(--border-color) !important;
}

:deep(.el-menu-item:hover) {
  color: var(--pink-primary) !important;
  background: rgba(252, 209, 219, 0.3) !important;
  border: 1px solid var(--pink-light) !important;
  transform: translateX(4px) !important;
  box-shadow: var(--shadow-md) !important;
  font-weight: 700 !important;
}

:deep(.el-menu-item.is-active) {
  color: var(--text-primary) !important;
  background: rgba(252, 174, 193, 0.4) !important;
  border: 2px solid var(--pink-primary) !important;
  box-shadow: var(--shadow-glow) !important;
  font-weight: 700 !important;
}

:deep(.el-sub-menu__title) {
  color: #9B8DC4 !important;
  background: rgba(255, 255, 255, 0.7) !important;
  border-radius: 12px !important;
  margin: 4px 8px !important;
  transition: all var(--transition-normal) !important;
  font-weight: 600 !important;
  border: 1px solid var(--border-color) !important;
}

:deep(.el-sub-menu__title:hover) {
  color: var(--pink-primary) !important;
  background: rgba(252, 209, 219, 0.25) !important;
  border: 1px solid var(--pink-light) !important;
  transform: translateX(2px) !important;
  box-shadow: var(--shadow-md) !important;
  font-weight: 700 !important;
}

:deep(.el-sub-menu .el-menu) {
  background: transparent !important;
}

:deep(.el-sub-menu .el-menu-item) {
  margin-left: 24px !important;
  padding-left: 16px !important;
  font-size: 13px !important;
  color: #A78BFA !important;
  background: rgba(255, 255, 255, 0.6) !important;
  font-weight: 500 !important;
}

:deep(.el-sub-menu .el-menu-item:hover) {
  color: var(--pink-primary) !important;
  background: rgba(252, 209, 219, 0.3) !important;
  font-weight: 600 !important;
}

:deep(.el-sub-menu .el-menu-item.is-active) {
  color: var(--text-primary) !important;
  background: rgba(252, 174, 193, 0.4) !important;
  border: 1px solid var(--pink-primary) !important;
  font-weight: 600 !important;
}

/* 主容器样式 */
.main-container {
  flex: 1;
  background: transparent;
}

/* 顶部导航栏样式 */
.header {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: var(--shadow-sm);
}

.header-left {
  display: flex;
  align-items: center;
}

.collapse-btn {
  margin-right: 20px;
  padding: 0;
  color: #606266;
}

.collapse-btn:hover {
  color: #409eff;
}

.breadcrumb {
  font-size: 14px;
}

:deep(.el-breadcrumb__inner) {
  color: #7C3AED;
  font-weight: 600;
}

:deep(.el-breadcrumb__inner.is-link:hover) {
  color: var(--pink-primary);
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 16px;
  transition: all var(--transition-normal);
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(15px);
  border: 1px solid var(--border-color);
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.user-avatar {
  margin-right: 8px;
}

.username {
  margin-right: 6px;
  font-size: 14px;
  color: #303133;
}

.dropdown-icon {
  font-size: 12px;
  color: #c0c4cc;
}

/* 主内容区域 */
.main-content {
  padding: 20px;
  overflow-y: auto;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>