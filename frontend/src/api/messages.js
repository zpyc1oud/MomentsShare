import request from './request'

export const messagesApi = {
  // 发送私信
  sendMessage(receiverId, content) {
    return request.post('/interactions/messages/', {
      receiver_id: receiverId,
      content
    })
  },

  // 获取会话列表
  getConversations() {
    return request.get('/interactions/messages/conversations/')
  },

  // 获取与指定用户的消息记录
  getMessageHistory(userId) {
    return request.get(`/interactions/messages/${userId}/`)
  },

  // 获取未读消息数
  getUnreadCount() {
    return request.get('/interactions/messages/unread/')
  }
}

export default messagesApi
