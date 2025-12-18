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
        // 使用真实后端API登录
        const response = await authAPI.login(credentials)

        if (response.access) {
          this.token = response.access
          this.userInfo = response.user_info

          // 保存到localStorage
          localStorage.setItem('admin_token', response.access)
          localStorage.setItem('admin_user_info', JSON.stringify(response.user_info))

          return { success: true }
        } else {
          return { success: false, message: '登录失败' }
        }
      } catch (error) {
        // 如果真实登录失败，提供友好的错误信息
        let errorMessage = '登录失败'

        if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        } else if (error.response?.status === 401) {
          errorMessage = '手机号或密码错误，或用户不是管理员'
        } else if (error.response?.status === 403) {
          errorMessage = '您没有管理员权限'
        }

        return {
          success: false,
          message: errorMessage
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