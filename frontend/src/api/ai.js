import request from './request'

// AI 请求需要更长的超时时间（GLM 模型可能需要 2 分钟）
const AI_TIMEOUT = 180000 // 3 分钟

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

    // 支持指定模型
    if (data.model) {
      formData.append('model', data.model)
    }

    return request.post('/ai/polish/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: AI_TIMEOUT
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

    // 支持指定模型
    if (data.model) {
      formData.append('model', data.model)
    }

    return request.post('/ai/recommend-tags/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: AI_TIMEOUT
    })
  }
}
