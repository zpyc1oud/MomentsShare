import request from './request'

export const usersApi = {
  // 获取当前用户信息
  getCurrentUser() {
    return request.get('/users/me/')
  },

  // 更新当前用户信息
  updateCurrentUser(data) {
    return request.put('/users/me/', data)
  },

  // 获取指定用户资料
  getUserProfile(userId) {
    return request.get(`/users/${userId}/`)
  }
}

export default usersApi
