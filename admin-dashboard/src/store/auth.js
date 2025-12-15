import { defineStore } from 'pinia'
import { authAPI } from '@/api/admin'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('admin_token') || null,
    userInfo: JSON.parse(localStorage.getItem('admin_user_info') || 'null'),
    isLoading: false
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userName: (state) => state.userInfo?.nickname || '管理员'
  },

  actions: {
    async login(credentials) {
      this.isLoading = true
      try {
        const response = await authAPI.login(credentials)

        this.token = response.access
        this.userInfo = response.user_info

        // 保存到localStorage
        localStorage.setItem('admin_token', response.access)
        localStorage.setItem('admin_user_info', JSON.stringify(response.user_info))

        return { success: true }
      } catch (error) {
        return {
          success: false,
          message: error.response?.data?.detail || '登录失败'
        }
      } finally {
        this.isLoading = false
      }
    },

    logout() {
      this.token = null
      this.userInfo = null

      // 清除localStorage
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user_info')
    },

    // 检查token是否有效
    checkAuth() {
      const token = localStorage.getItem('admin_token')
      const userInfo = localStorage.getItem('admin_user_info')

      if (token && userInfo) {
        this.token = token
        this.userInfo = JSON.parse(userInfo)
        return true
      }
      return false
    }
  }
})