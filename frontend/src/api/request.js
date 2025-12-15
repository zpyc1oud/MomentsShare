import axios from 'axios'
import router from '@/router'

// 创建 axios 实例
const request = axios.create({
  baseURL: '/api/v1',
  timeout: 15000,
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
          localStorage.setItem('access_token', newToken)
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          
          return request(originalRequest)
        } catch (refreshError) {
          // 刷新失败，清除 token 并跳转登录
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          router.push({ name: 'Login' })
        }
      } else {
        router.push({ name: 'Login' })
      }
    }
    
    return Promise.reject(error)
  }
)

export default request

