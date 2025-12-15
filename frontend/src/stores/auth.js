import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token') || '')
  const refreshToken = ref(localStorage.getItem('refresh_token') || '')

  // Getters
  const isLoggedIn = computed(() => !!accessToken.value)
  const userInfo = computed(() => user.value)

  // Actions
  const setTokens = (access, refresh) => {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  }

  const clearTokens = () => {
    accessToken.value = ''
    refreshToken.value = ''
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  const login = async (phone, password) => {
    try {
      const response = await authApi.login({ phone, password })
      setTokens(response.access, response.refresh)
      user.value = response.user_info
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail?.detail?.[0] || '登录失败' 
      }
    }
  }

  const register = async (data) => {
    try {
      const response = await authApi.register(data)
      return { success: true, data: response }
    } catch (error) {
      const errors = error.response?.data?.detail || {}
      const message = Object.values(errors).flat()[0] || '注册失败'
      return { success: false, message }
    }
  }

  const logout = async () => {
    try {
      if (refreshToken.value) {
        await authApi.logout({ refresh_token: refreshToken.value })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      clearTokens()
    }
  }

  const fetchUserInfo = async () => {
    try {
      const response = await authApi.getUserInfo()
      user.value = response
      return response
    } catch (error) {
      console.error('Fetch user info error:', error)
      return null
    }
  }

  return {
    // State
    user,
    accessToken,
    refreshToken,
    // Getters
    isLoggedIn,
    userInfo,
    // Actions
    setTokens,
    clearTokens,
    login,
    register,
    logout,
    fetchUserInfo
  }
})

