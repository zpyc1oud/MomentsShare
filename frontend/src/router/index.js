import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 路由配置
const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  // P1: 登录/注册
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginPage.vue'),
    meta: { requiresAuth: false, hideTabbar: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/RegisterPage.vue'),
    meta: { requiresAuth: false, hideTabbar: true }
  },
  // P2: 首页 Feed 流
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/views/home/HomePage.vue'),
    meta: { requiresAuth: true }
  },
  // P3: 发布页
  {
    path: '/publish',
    name: 'Publish',
    component: () => import('@/views/publish/PublishPage.vue'),
    meta: { requiresAuth: true, hideTabbar: true }
  },
  // P4: 发现与搜索
  {
    path: '/discover',
    name: 'Discover',
    component: () => import('@/views/discover/DiscoverPage.vue'),
    meta: { requiresAuth: true }
  },
  // P5: 消息与好友
  {
    path: '/messages',
    name: 'Messages',
    component: () => import('@/views/messages/MessagesPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/friends',
    name: 'Friends',
    component: () => import('@/views/messages/FriendsPage.vue'),
    meta: { requiresAuth: true, hideTabbar: true }
  },
  {
    path: '/friend-requests',
    name: 'FriendRequests',
    component: () => import('@/views/messages/FriendRequestsPage.vue'),
    meta: { requiresAuth: true, hideTabbar: true }
  },
  {
    path: '/add-friend',
    name: 'AddFriend',
    component: () => import('@/views/messages/AddFriendPage.vue'),
    meta: { requiresAuth: true, hideTabbar: true }
  },
  {
    path: '/chat/:userId',
    name: 'Chat',
    component: () => import('@/views/messages/ChatPage.vue'),
    meta: { requiresAuth: true, hideTabbar: true }
  },
  // P6: 动态详情
  {
    path: '/moment/:id',
    name: 'MomentDetail',
    component: () => import('@/views/moment/MomentDetailPage.vue'),
    meta: { requiresAuth: true, hideTabbar: true }
  },
  // P7: 个人中心
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/profile/ProfilePage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile/edit',
    name: 'ProfileEdit',
    component: () => import('@/views/profile/ProfileEditPage.vue'),
    meta: { requiresAuth: true, hideTabbar: true }
  },
  {
    path: '/user/:id',
    name: 'UserProfile',
    component: () => import('@/views/profile/UserProfilePage.vue'),
    meta: { requiresAuth: true, hideTabbar: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/profile/SettingsPage.vue'),
    meta: { requiresAuth: true, hideTabbar: true }
  },
  // 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/NotFoundPage.vue'),
    meta: { requiresAuth: false, hideTabbar: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 需要登录但未登录
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }
  
  // 已登录但访问登录页
  if (authStore.isLoggedIn && (to.name === 'Login' || to.name === 'Register')) {
    next({ name: 'Home' })
    return
  }
  
  next()
})

export default router

