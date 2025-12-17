import request from './request'

export const aiApi = {
  // 文案润色
  polish(data) {
    const formData = new FormData()
    
    if (data.text) {
      formData.append('text', data.text)
    }
    
    if (data.image) {
      formData.append('image', data.image)
    }
    
    return request.post('/ai/polish/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 标签推荐
  recommendTags(data) {
    const formData = new FormData()
    
    if (data.text) {
      formData.append('text', data.text)
    }
    
    if (data.image) {
      formData.append('image', data.image)
    }
    
    return request.post('/ai/recommend-tags/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}

