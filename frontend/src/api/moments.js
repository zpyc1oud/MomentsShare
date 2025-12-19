import request from './request'

export const momentsApi = {
  // 发布动态
  create(data) {
    const formData = new FormData()
    
    // 添加文本内容
    if (data.content) {
      formData.append('content', data.content)
    }
    
    // 添加类型
    formData.append('type', data.type)
    
    // 添加图片（多个）
    if (data.images && data.images.length > 0) {
      data.images.forEach((image) => {
        formData.append('images', image)
      })
    }
    
    // 添加视频
    if (data.video) {
      formData.append('video', data.video)
    }
    
    // 添加标签
    if (data.labels && data.labels.length > 0) {
      data.labels.forEach((label) => {
        formData.append('labels', label)
      })
    }
    
    return request.post('/moments/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 获取动态详情
  getDetail(id) {
    return request.get(`/moments/${id}/`)
  },

  // 获取好友动态流
  getFeed(page = 1) {
    return request.get('/moments/feed/', { params: { page } })
  },

  // 获取我的动态列表
  getMyMoments(page = 1) {
    return request.get('/moments/my/', { params: { page } })
  },

  // 搜索动态
  search(params) {
    return request.get('/moments/search/', { params })
  },

  // 获取评论列表
  getComments(momentId, page = 1) {
    return request.get(`/moments/${momentId}/comments/`, { params: { page } })
  },

  // 发布评论
  createComment(momentId, data) {
    return request.post(`/moments/${momentId}/comments/`, data)
  },

  // 点赞/取消点赞
  toggleLike(momentId) {
    return request.post(`/moments/${momentId}/like/`)
  }
}

