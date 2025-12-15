import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

/**
 * 格式化时间为相对时间
 * @param {string|Date} time 
 * @returns {string}
 */
export const formatRelativeTime = (time) => {
  return dayjs(time).fromNow()
}

/**
 * 格式化日期
 * @param {string|Date} time 
 * @param {string} format 
 * @returns {string}
 */
export const formatDate = (time, format = 'YYYY-MM-DD HH:mm') => {
  return dayjs(time).format(format)
}

/**
 * 手机号脱敏
 * @param {string} phone 
 * @returns {string}
 */
export const maskPhone = (phone) => {
  if (!phone) return ''
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

/**
 * 验证手机号格式
 * @param {string} phone 
 * @returns {boolean}
 */
export const isValidPhone = (phone) => {
  return /^1\d{10}$/.test(phone)
}

/**
 * 防抖函数
 * @param {Function} fn 
 * @param {number} delay 
 * @returns {Function}
 */
export const debounce = (fn, delay = 300) => {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

/**
 * 节流函数
 * @param {Function} fn 
 * @param {number} interval 
 * @returns {Function}
 */
export const throttle = (fn, interval = 300) => {
  let lastTime = 0
  return function (...args) {
    const now = Date.now()
    if (now - lastTime >= interval) {
      lastTime = now
      fn.apply(this, args)
    }
  }
}

/**
 * 复制文本到剪贴板
 * @param {string} text 
 * @returns {Promise<boolean>}
 */
export const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch (error) {
    console.error('Copy failed:', error)
    return false
  }
}

/**
 * 获取文件扩展名
 * @param {string} filename 
 * @returns {string}
 */
export const getFileExtension = (filename) => {
  return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2)
}

/**
 * 判断是否为图片文件
 * @param {File|string} file 
 * @returns {boolean}
 */
export const isImageFile = (file) => {
  const imageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
  if (file instanceof File) {
    return imageTypes.includes(file.type)
  }
  const ext = getFileExtension(file).toLowerCase()
  return ['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext)
}

/**
 * 判断是否为视频文件
 * @param {File|string} file 
 * @returns {boolean}
 */
export const isVideoFile = (file) => {
  const videoTypes = ['video/mp4', 'video/quicktime', 'video/webm']
  if (file instanceof File) {
    return videoTypes.includes(file.type)
  }
  const ext = getFileExtension(file).toLowerCase()
  return ['mp4', 'mov', 'webm'].includes(ext)
}

