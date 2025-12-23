import axios from 'axios'
import router from '@/router'

// 创建 axios 实例
const request = axios.create({
  baseURL: '/api/v1',
  timeout: 120000, // 默认 60 秒（适合大多数 API）
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  async (error) => {
    const originalRequest = error.config
    
    // Token 过期，尝试刷新
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post('/api/v1/auth/token/refresh/', {
            refresh: refreshToken
          })
          
          const newToken = response.data.access
          // 同步更新 Pinia 中的 token 状态，保持与 localStorage 一致
          try {
            const { useAuthStore } = await import('@/stores/auth')
            const authStore = useAuthStore()
            authStore.setTokens(newToken, refreshToken)
          } catch (e) {
            // 如果 Pinia 尚未初始化，则至少保证 localStorage 中的 token 是最新的
            localStorage.setItem('access_token', newToken)
          }

          originalRequest.headers.Authorization = `Bearer ${newToken}`
          
          return request(originalRequest)
        } catch (refreshError) {
          // 刷新失败，清除登录状态并跳转登录页
          try {
            const { useAuthStore } = await import('@/stores/auth')
            const authStore = useAuthStore()
            authStore.clearTokens()
          } catch (e) {
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
          }

          router.push({
            name: 'Login',
            query: { redirect: router.currentRoute.value.fullPath, message: '登录已过期，请重新登录' }
          })
        }
      } else {
        router.push({
          name: 'Login',
          query: { redirect: router.currentRoute.value.fullPath, message: '请先登录' }
        })
      }
    }
    
    return Promise.reject(error)
  }
)

export default request

