import request from './request'

export const friendsApi = {
  // 发起好友申请
  sendRequest(toUserId) {
    return request.post('/friends/request/', { to_user_id: toUserId })
  },

  // 响应好友申请
  respondRequest(requestId, action) {
    return request.post('/friends/respond/', { request_id: requestId, action })
  },

  // 删除好友
  deleteFriend(userId) {
    return request.delete(`/friends/${userId}/`)
  },

  // 获取好友列表
  getFriendList(page = 1) {
    return request.get('/friends/', { params: { page } })
  },

  // 搜索用户
  searchUsers(keyword, page = 1) {
    return request.get('/friends/search/', { params: { keyword, page } })
  },

  // 获取待处理的好友申请
  getPendingRequests() {
    return request.get('/friends/pending/')
  }
}

