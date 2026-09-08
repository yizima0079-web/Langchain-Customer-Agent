// utils/api.js 请求封装
const BASE_URL = 'http://127.0.0.1:8000/api/v1'
// 静态资源地址（图片等）
const STATIC_URL = 'http://127.0.0.1:8000'

/** 通用请求函数 */
function request(url, method = 'GET', data = {}) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: BASE_URL + url,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + (wx.getStorageSync('token') || ''),
      },
      success(res) {
        if (res.statusCode === 200) {
          const body = res.data
          if (body.code === 0) {
            resolve(body.data)
          } else {
            wx.showToast({ title: body.message || '请求失败', icon: 'none' })
            reject(body)
          }
        } else if (res.statusCode === 401) {
          wx.removeStorageSync('token')
          wx.showToast({ title: '请先登录', icon: 'none' })
          reject(res)
        } else {
          wx.showToast({ title: (res.data && res.data.detail) || '网络错误', icon: 'none' })
          reject(res)
        }
      },
      fail(err) {
        wx.showToast({ title: '网络异常，请检查后端服务', icon: 'none' })
        reject(err)
      },
    })
  })
}

/** 流式聊天：接收后端 SSE 分片并逐段回调 */
function streamChat(data, onEvent) {
  return new Promise((resolve, reject) => {
    let buffer = ''
    let fallbackStarted = false
    let receivedEvent = false
    const decoder = typeof TextDecoder !== 'undefined' ? new TextDecoder('utf-8') : null
    const parse = (text) => {
      buffer += text
      const events = buffer.split('\n\n')
      buffer = events.pop() || ''
      events.forEach((event) => {
        const line = event.split('\n').find((item) => item.indexOf('data:') === 0)
        if (!line) return
        try {
          receivedEvent = true
          onEvent(JSON.parse(line.slice(5).trim()))
        } catch (e) { /* 等待完整分片 */ }
      })
    }
    const fallback = () => {
      if (fallbackStarted) return
      fallbackStarted = true
      request('/chat', 'POST', data).then((res) => {
        onEvent({ type: 'meta', session_id: res.session_id })
        const answer = res.answer || ''
        for (let i = 0; i < answer.length; i += 3) {
          onEvent({ type: 'delta', content: answer.slice(i, i + 3) })
        }
        onEvent({ type: 'done' })
        resolve(res)
      }).catch(reject)
    }
    wx.request({
      url: BASE_URL + '/chat/stream',
      method: 'POST',
      data,
      enableChunked: true,
      header: {
        'Content-Type': 'application/json',
        Accept: 'text/event-stream',
        Authorization: 'Bearer ' + (wx.getStorageSync('token') || ''),
      },
      onChunkReceived(res) {
        if (decoder) parse(decoder.decode(res.data, { stream: true }))
        else parse(decodeURIComponent(escape(String.fromCharCode.apply(null, new Uint8Array(res.data)))))
      },
      success(res) {
        if (res.statusCode !== 200) {
          fallback()
          return
        }
        // 部分基础库不触发 onChunkReceived，会把流式响应一次性放在 res.data。
        if (typeof res.data === 'string') parse(res.data)
        if (receivedEvent) resolve(res)
        else fallback()
      },
      fail: fallback,
    })
  })
}

module.exports = {
  get: (url, data) => request(url, 'GET', data),
  post: (url, data) => request(url, 'POST', data),
  streamChat,
  put: (url, data) => request(url, 'PUT', data),
  del: (url, data) => request(url, 'DELETE', data),
  // 拼接静态资源完整地址
  fullUrl: (path) => (path && path.startsWith('http') ? path : STATIC_URL + path),
}
