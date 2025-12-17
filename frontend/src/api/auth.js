import request from './request'

export const authApi = {
  // 用户注册
  register(data) {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      if (data[key] !== undefined && data[key] !== null) {
        formData.append(key, data[key])
      }
    })
    return request.post('/auth/register/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 用户登录
  login(data) {
    return request.post('/auth/login/', data)
  },

  // 用户登出
  logout(data) {
    return request.post('/auth/logout/', data)
  },

  // 获取当前用户信息
  getUserInfo() {
    return request.get('/users/me/')
  },

  // 更新用户信息
  updateUserInfo(data) {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      if (data[key] !== undefined && data[key] !== null) {
        formData.append(key, data[key])
      }
    })
    return request.patch('/users/me/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 更换手机号
  changePhone(data) {
    return request.post('/users/me/phone/', data)
  }
}

