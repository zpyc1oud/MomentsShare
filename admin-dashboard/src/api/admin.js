import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'

// 创建axios实例
const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const authStore = useAuthStore()

    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 401:
          ElMessage.error('未授权，请重新登录')
          authStore.logout()
          break
        case 403:
          ElMessage.error('无权限访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(data?.detail || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络连接失败')
    } else {
      ElMessage.error('请求配置错误')
    }

    return Promise.reject(error)
  }
)

// 管理员认证相关API
export const authAPI = {
  // 管理员登录
  login: (credentials) => {
    return api.post('/admin/auth/login/', credentials)
  }
}

// 统计数据相关API
export const statisticsAPI = {
  // 获取综合统计数据（近7日）- 包含DAU、新增用户、发帖数
  getAllStats: () => {
    return api.get('/admin/stats/')
  },

  // 从综合数据中提取用户增长趋势
  getUserTrend: () => {
    return api.get('/admin/stats/').then(data => {
      return data.map(item => ({
        date: item.date,
        count: item.daily_new_users
      }))
    })
  },

  // 从综合数据中提取DAU数据
  getDAUTrend: () => {
    return api.get('/admin/stats/').then(data => {
      return data.map(item => ({
        date: item.date,
        count: item.dau
      }))
    })
  },

  // 生成内容类型分布数据（基于发帖数）
  getContentDistribution: () => {
    return api.get('/admin/stats/').then(data => {
      // 计算总发帖数和模拟内容分布
      const totalPosts = data.reduce((sum, item) => sum + item.daily_posts, 0)

      // 基于实际数据的模拟分布
      return [
        { type: '图文动态', count: Math.floor(totalPosts * 0.6) },
        { type: '视频动态', count: Math.floor(totalPosts * 0.25) },
        { type: '纯文字', count: Math.floor(totalPosts * 0.1) },
        { type: '转发', count: Math.floor(totalPosts * 0.05) }
      ]
    })
  }
}

// 内容管理相关API
export const contentAPI = {
  // 获取内容列表
  getContentList: (params) => {
    return api.get('/admin/contents/', { params })
  },

  // 下架内容
  deleteContent: (id) => {
    return api.delete(`/admin/contents/${id}/`)
  }
}

export default api